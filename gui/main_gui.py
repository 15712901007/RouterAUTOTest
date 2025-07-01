# gui/main_gui.py

import sys
import subprocess
import os
import shutil
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QCheckBox, QGroupBox, QTextEdit, QLabel)
from PyQt6.QtCore import QThread, pyqtSignal, QObject
from PyQt6.QtGui import QFont

# 获取项目根目录
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Worker(QObject):
    """
    将耗时的测试任务放在工作线程中，执行完整的测试流程。
    """
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def run(self):
        try:
            # --- 步骤 1: 清理旧的Allure结果 (Python方式) ---
            self.progress.emit("[1/4] 清理旧的测试结果...")
            allure_results_dir = os.path.join(project_root, 'reports', 'allure_results')
            if os.path.exists(allure_results_dir):
                shutil.rmtree(allure_results_dir)
            os.makedirs(allure_results_dir)

            # --- 步骤 2: 直接执行 Pytest ---
            self.progress.emit("[2/4] 开始执行Pytest测试...")
            pytest_cmd = [
                'pytest', os.path.join(project_root, 'tests'),
                '--alluredir=' + allure_results_dir,
                '--screenshot=only-on-failure', '--video=retain-on-failure'
            ]
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            process = subprocess.Popen(
                pytest_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding='utf-8', errors='replace',
                cwd=project_root, env=env
            )
            for line in iter(process.stdout.readline, ''):
                self.progress.emit(line.strip())
            return_code = process.wait()
            if return_code != 0:
                self.progress.emit("\n******* 测试执行失败! *******")
            else:
                self.progress.emit("\n******* 测试执行成功! *******")

            # --- 步骤 3: 生成 Allure 报告 ---
            self.progress.emit("[3/4] 生成标准Allure报告...")
            allure_report_dir = os.path.join(project_root, 'reports', 'allure_report')
            generate_cmd = [
                'allure', 'generate', allure_results_dir,
                '-o', allure_report_dir, '--clean'
            ]
            # 【关键修复】添加 shell=True，让系统shell去寻找allure命令
            subprocess.run(generate_cmd, cwd=project_root, capture_output=True, shell=True)
            self.progress.emit("报告生成完毕。")

            # --- 步骤 4: 打开 Allure 报告 ---
            self.progress.emit("[4/4] 正在打开Allure报告...")
            open_cmd = ['allure', 'open', allure_report_dir]
            # 【关键修复】同样添加 shell=True
            subprocess.Popen(open_cmd, cwd=project_root, shell=True)

        except FileNotFoundError as e:
            # 这个错误现在主要针对pytest，因为allure已经通过shell执行
            self.progress.emit(f"\n--- 发生错误 --- \n命令未找到: {e.filename}")
            self.progress.emit("请确保 pytest 已经安装并配置在系统的PATH环境变量中。")
        except Exception as e:
            self.progress.emit(f"\n--- 发生错误 --- \n{e}")
        finally:
            self.progress.emit("\n--- 测试执行完毕 ---")
            self.finished.emit()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('路由器UI自动化测试平台 (PyQt6)')
        self.setGeometry(300, 300, 800, 600) # 稍微加宽一点窗口
        main_layout = QVBoxLayout()
        group_box = QGroupBox('测试模块选择')
        group_layout = QVBoxLayout()
        self.vlan_checkbox = QCheckBox('VLAN 功能测试')
        self.vlan_checkbox.setChecked(True)
        group_layout.addWidget(self.vlan_checkbox)
        port_map_checkbox = QCheckBox('端口映射测试 (待实现)')
        port_map_checkbox.setEnabled(False)
        group_layout.addWidget(port_map_checkbox)
        acl_checkbox = QCheckBox('ACL规则测试 (待实现)')
        acl_checkbox.setEnabled(False)
        group_layout.addWidget(acl_checkbox)
        group_box.setLayout(group_layout)
        main_layout.addWidget(group_box)
        self.run_button = QPushButton('开始测试')
        self.run_button.clicked.connect(self.run_tests)
        main_layout.addWidget(self.run_button)
        main_layout.addWidget(QLabel('测试输出:'))
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Consolas", 10))
        main_layout.addWidget(self.output_text)
        self.setLayout(main_layout)

    def run_tests(self):
        self.output_text.clear()
        self.run_button.setEnabled(False)
        self.run_button.setText('测试运行中...')
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.update_output)
        self.thread.finished.connect(self.on_test_finished)
        self.thread.start()

    def update_output(self, text):
        self.output_text.append(text)

    def on_test_finished(self):
        self.run_button.setEnabled(True)
        self.run_button.setText('开始测试')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())