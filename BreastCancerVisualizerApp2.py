# Breast Cancer Visualizer App — BAR CHART VERSION
# Requires: wxPython, pandas, matplotlib

import wx
import pandas as pd
import matplotlib.pyplot as plt

# Adjust these to match your breast_data.csv columns
FEATURE_Y = "tumorsizenum"     # Tumor size
LABEL_COL = "class"            # Class: recurrence / no recurrence

class BreastVisualizerApp(wx.Frame):
    def __init__(self, parent=None, title="Breast Cancer Dataset Visualizer"):
        super().__init__(parent, title=title, size=(820, 520))
        self.SetMinSize((760, 480))
        panel = wx.Panel(self)

        open_btn = wx.Button(panel, label="Open Breast Cancer Dataset…")
        font = open_btn.GetFont()
        font.PointSize += 2
        open_btn.SetFont(font)
        open_btn.Bind(wx.EVT_BUTTON, self.on_open)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer(1)
        sizer.Add(open_btn, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        sizer.AddStretchSpacer(2)
        panel.SetSizer(sizer)

        self.Centre()
        self.Show()

    def on_open(self, _evt):
        with wx.FileDialog(
            self,
            "Open Breast Cancer CSV",
            wildcard="CSV files (*.csv)|*.csv",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        ) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return
            path = dlg.GetPath()

        try:
            df = pd.read_csv(path)

            # Normalize headers
            df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]

            # Auto rename if only 3 columns exist
            if df.shape[1] == 3:
                df.columns = ["class", "deg-malig", "tumorsizenum"]

            # Verify required columns
            for col in [FEATURE_Y, LABEL_COL]:
                if col not in df.columns:
                    raise ValueError(
                        "CSV must contain 'Class' and 'TumorSizeNum' columns."
                    )

            # Pretty label formatting
            def pretty(name: str) -> str:
                return name.replace("_", " ").replace("-", " ").title()

            # ---- SIMPLE BAR CHART ----
            # Compute mean tumor size per class
            stats = (
                df.groupby(LABEL_COL)[FEATURE_Y]
                .mean()
                .sort_values(ascending=False)
            )

            plt.figure(figsize=(7.5, 5.0))
            stats.plot(kind="bar", color=["salmon", "skyblue"])

            plt.title(
                f"Breast Cancer: Mean {pretty(FEATURE_Y)} by Class"
            )
            plt.xlabel("Class")
            plt.ylabel(f"Mean {pretty(FEATURE_Y)}")
            plt.grid(axis="y", linestyle="--", alpha=0.3)
            plt.tight_layout()
            plt.show()

        except Exception as e:
            wx.MessageBox(
                f"Error loading or plotting file:\n{e}",
                "Error",
                wx.OK | wx.ICON_ERROR,
            )

if __name__ == "__main__":
    app = wx.App(False)
    BreastVisualizerApp()
    app.MainLoop()
