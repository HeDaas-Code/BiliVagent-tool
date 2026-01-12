#!/usr/bin/env python3
"""
BiliVagent - Bilibili Video Analysis Agent
GUI interface using Tkinter
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import sys
import io
import json
import os


class TextRedirector:
    """Redirect stdout to a tkinter Text widget"""
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.buffer = io.StringIO()
        self.encoding = 'utf-8'  # Add encoding attribute for yt-dlp compatibility

    def write(self, string):
        # Handle None input
        if string is None:
            return

        # Handle bytes input
        if isinstance(string, bytes):
            try:
                string = string.decode('utf-8')
            except UnicodeDecodeError:
                string = string.decode('utf-8', errors='replace')

        # Ensure string type
        if not isinstance(string, str):
            string = str(string)

        try:
            self.buffer.write(string)
            # Use after() for thread-safe GUI updates
            self.text_widget.after(0, self._update_text, string)
        except Exception:
            pass  # Silently ignore write errors

    def _update_text(self, string):
        """Thread-safe text update"""
        try:
            self.text_widget.configure(state='normal')
            self.text_widget.insert(tk.END, string)
            self.text_widget.see(tk.END)
            self.text_widget.configure(state='disabled')
        except Exception:
            pass  # Silently ignore GUI errors

    def flush(self):
        pass

    def isatty(self):
        """Return False to indicate this is not a TTY"""
        return False


class BiliVagentGUI:
    """Main GUI Application for BiliVagent"""

    def __init__(self, root):
        self.root = root
        self.root.title("BiliVagent - Bilibili视频智能分析工具")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)

        # Set theme colors
        self.bg_color = "#f5f5f5"
        self.primary_color = "#00a1d6"  # Bilibili pink-blue
        self.accent_color = "#fb7299"   # Bilibili pink

        self.root.configure(bg=self.bg_color)

        # Initialize agent as None
        self.agent = None
        self.current_report = None
        self.is_analyzing = False

        self._create_widgets()
        self._setup_layout()

    def _create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")

        # Title Label
        self.title_frame = ttk.Frame(self.main_frame)
        self.title_label = ttk.Label(
            self.title_frame,
            text="🎬 BiliVagent - Bilibili视频智能分析工具",
            font=("Microsoft YaHei", 16, "bold")
        )

        # Input Frame
        self.input_frame = ttk.LabelFrame(self.main_frame, text="视频输入", padding="10")

        self.url_label = ttk.Label(self.input_frame, text="视频链接/BV号:")
        self.url_entry = ttk.Entry(self.input_frame, width=60, font=("Microsoft YaHei", 10))
        self.url_entry.insert(0, "请输入Bilibili视频链接或BV号")
        self.url_entry.bind("<FocusIn>", self._clear_placeholder)
        self.url_entry.bind("<FocusOut>", self._restore_placeholder)
        self.url_entry.bind("<Return>", lambda e: self._start_analysis())

        # Style for buttons
        style = ttk.Style()
        style.configure("Primary.TButton", font=("Microsoft YaHei", 10))
        style.configure("Accent.TButton", font=("Microsoft YaHei", 10))

        self.analyze_btn = ttk.Button(
            self.input_frame,
            text="🔍 开始分析",
            command=self._start_analysis,
            style="Primary.TButton"
        )

        self.stop_btn = ttk.Button(
            self.input_frame,
            text="⏹ 停止",
            command=self._stop_analysis,
            state="disabled",
            style="Accent.TButton"
        )

        # Progress Frame
        self.progress_frame = ttk.Frame(self.main_frame)
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='indeterminate',
            length=300
        )
        self.status_label = ttk.Label(
            self.progress_frame,
            text="就绪",
            font=("Microsoft YaHei", 9)
        )

        # Notebook for output tabs
        self.notebook = ttk.Notebook(self.main_frame)

        # Log Tab
        self.log_frame = ttk.Frame(self.notebook, padding="5")
        self.log_text = scrolledtext.ScrolledText(
            self.log_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            state='disabled',
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="white"
        )

        # Report Tab
        self.report_frame = ttk.Frame(self.notebook, padding="5")
        self.report_text = scrolledtext.ScrolledText(
            self.report_frame,
            wrap=tk.WORD,
            font=("Microsoft YaHei", 10),
            state='disabled',
            bg="white"
        )

        # Add tabs to notebook
        self.notebook.add(self.log_frame, text="📋 运行日志")
        self.notebook.add(self.report_frame, text="📊 分析报告")

        # Bottom Frame - Actions
        self.action_frame = ttk.Frame(self.main_frame)

        self.save_btn = ttk.Button(
            self.action_frame,
            text="💾 保存报告",
            command=self._save_report,
            state="disabled"
        )

        self.clear_btn = ttk.Button(
            self.action_frame,
            text="🗑 清空日志",
            command=self._clear_log
        )

        self.exit_btn = ttk.Button(
            self.action_frame,
            text="❌ 退出",
            command=self._on_exit
        )

    def _setup_layout(self):
        """Setup widget layout"""
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        self.title_frame.pack(fill=tk.X, pady=(0, 10))
        self.title_label.pack()

        # Input Frame
        self.input_frame.pack(fill=tk.X, pady=(0, 10))
        self.url_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.url_entry.grid(row=0, column=1, sticky=tk.EW, padx=(0, 10))
        self.analyze_btn.grid(row=0, column=2, padx=(0, 5))
        self.stop_btn.grid(row=0, column=3)
        self.input_frame.columnconfigure(1, weight=1)

        # Progress Frame
        self.progress_frame.pack(fill=tk.X, pady=(0, 10))
        self.status_label.pack(side=tk.LEFT, padx=(0, 10))
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Notebook
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.report_text.pack(fill=tk.BOTH, expand=True)

        # Action Frame
        self.action_frame.pack(fill=tk.X)
        self.save_btn.pack(side=tk.LEFT, padx=(0, 5))
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 5))
        self.exit_btn.pack(side=tk.RIGHT)

    def _clear_placeholder(self, event):
        """Clear placeholder text on focus"""
        if self.url_entry.get() == "请输入Bilibili视频链接或BV号":
            self.url_entry.delete(0, tk.END)

    def _restore_placeholder(self, event):
        """Restore placeholder if empty"""
        if not self.url_entry.get():
            self.url_entry.insert(0, "请输入Bilibili视频链接或BV号")

    def _start_analysis(self):
        """Start video analysis in a separate thread"""
        url = self.url_entry.get().strip()

        if not url or url == "请输入Bilibili视频链接或BV号":
            messagebox.showwarning("输入错误", "请输入有效的Bilibili视频链接或BV号")
            return

        if self.is_analyzing:
            messagebox.showinfo("提示", "分析正在进行中，请稍候...")
            return

        # Clear previous output
        self._clear_log()
        self._clear_report()

        # Update UI state
        self.is_analyzing = True
        self.analyze_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.save_btn.configure(state="disabled")
        self.progress_bar.start(10)
        self.status_label.configure(text="正在分析...")

        # Redirect stdout to log
        self.old_stdout = sys.stdout
        sys.stdout = TextRedirector(self.log_text)

        # Run analysis in background thread
        self.analysis_thread = threading.Thread(
            target=self._run_analysis,
            args=(url,),
            daemon=True
        )
        self.analysis_thread.start()

    def _run_analysis(self, url):
        """Run the actual analysis (in background thread)"""
        try:
            # Import here to avoid circular imports and allow lazy loading
            from bilivagent.agents.bilivagent import BiliVagent

            if self.agent is None:
                print("正在初始化分析引擎...")
                self.agent = BiliVagent()

            report = self.agent.analyze_video(url)
            self.current_report = report

            # Update UI from main thread
            self.root.after(0, lambda: self._analysis_complete(report))

        except Exception as e:
            import traceback
            error_msg = f"分析错误: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            self.root.after(0, lambda: self._analysis_failed(str(e)))

    def _analysis_complete(self, report):
        """Called when analysis is complete"""
        self.is_analyzing = False
        self.analyze_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.save_btn.configure(state="normal")
        self.progress_bar.stop()
        self.status_label.configure(text="✅ 分析完成")

        # Restore stdout
        sys.stdout = self.old_stdout

        # Display report
        self._display_report(report)

        # Switch to report tab
        self.notebook.select(1)

        messagebox.showinfo("完成", "视频分析完成！")

    def _analysis_failed(self, error):
        """Called when analysis fails"""
        self.is_analyzing = False
        self.analyze_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.progress_bar.stop()
        self.status_label.configure(text="❌ 分析失败")

        # Restore stdout
        sys.stdout = self.old_stdout

        messagebox.showerror("错误", f"分析失败:\n{error}")

    def _stop_analysis(self):
        """Stop the current analysis (not fully implemented - threads can't be killed easily)"""
        if self.is_analyzing:
            messagebox.showinfo("提示", "正在停止分析...请稍候")
            # Note: Python threads can't be forcefully killed
            # This just updates the UI state
            self.is_analyzing = False
            self.analyze_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            self.progress_bar.stop()
            self.status_label.configure(text="已停止")

    def _display_report(self, report):
        """Display the analysis report in the report tab"""
        self.report_text.configure(state='normal')
        self.report_text.delete(1.0, tk.END)

        # Format report
        text = "=" * 60 + "\n"
        text += "分析报告\n"
        text += "=" * 60 + "\n\n"

        text += f"🎬 BV号: {report.get('BV号', 'N/A')}\n"
        text += f"📺 视频标题: {report.get('视频标题', 'N/A')}\n\n"

        text += "📝 概述:\n"
        text += f"{report.get('概述', 'N/A')}\n\n"

        text += "🏷️ 关键词（前十）:\n"
        keywords = report.get('关键词（前十）', [])
        for i, keyword in enumerate(keywords, 1):
            text += f"  {i}. {keyword}\n"
        text += "\n"

        text += f"🎨 视频风格: {report.get('视频风格', 'N/A')}\n\n"

        text += f"💬 讨论情感: {report.get('讨论情感', 'N/A')}\n\n"

        text += "💡 讨论关键词:\n"
        comment_keywords = report.get('讨论关键词', [])
        for i, keyword in enumerate(comment_keywords, 1):
            text += f"  {i}. {keyword}\n"
        text += "\n"

        text += "🗣️ 相关讨论:\n"
        text += f"{report.get('相关讨论', 'N/A')}\n\n"

        text += "📊 元数据:\n"
        metadata = report.get('元数据', {})
        text += f"  分区: {metadata.get('分区', 'N/A')}\n"
        text += f"  UP主: {metadata.get('UP主', 'N/A')}\n"
        text += f"  时长: {metadata.get('时长', 'N/A')}秒\n"
        text += f"  评论数: {metadata.get('评论数', 0)}\n"
        text += f"  弹幕数: {metadata.get('弹幕数', 0)}\n"

        text += "\n" + "=" * 60 + "\n"

        self.report_text.insert(tk.END, text)
        self.report_text.configure(state='disabled')

    def _save_report(self):
        """Save the current report to a file"""
        if not self.current_report:
            messagebox.showwarning("警告", "没有可保存的报告")
            return

        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[
                ("JSON文件", "*.json"),
                ("文本文件", "*.txt"),
                ("所有文件", "*.*")
            ],
            initialfile=f"{self.current_report.get('BV号', 'report')}_report.json"
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    if file_path.endswith('.json'):
                        json.dump(self.current_report, f, ensure_ascii=False, indent=2)
                    else:
                        # Save as text
                        self.report_text.configure(state='normal')
                        f.write(self.report_text.get(1.0, tk.END))
                        self.report_text.configure(state='disabled')

                messagebox.showinfo("成功", f"报告已保存到:\n{file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败:\n{str(e)}")

    def _clear_log(self):
        """Clear the log text"""
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state='disabled')

    def _clear_report(self):
        """Clear the report text"""
        self.report_text.configure(state='normal')
        self.report_text.delete(1.0, tk.END)
        self.report_text.configure(state='disabled')
        self.current_report = None

    def _on_exit(self):
        """Handle exit"""
        if self.is_analyzing:
            if not messagebox.askyesno("确认", "分析正在进行中，确定要退出吗？"):
                return
        self.root.quit()
        self.root.destroy()


def main():
    """Main entry point for GUI"""
    root = tk.Tk()

    # Set icon if available
    try:
        # You can add an icon file here
        pass
    except:
        pass

    app = BiliVagentGUI(root)

    # Handle window close
    root.protocol("WM_DELETE_WINDOW", app._on_exit)

    root.mainloop()


if __name__ == "__main__":
    main()
