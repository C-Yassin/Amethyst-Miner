from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QCheckBox, QStyleOptionButton, QStyle,QSizePolicy
from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath, QLinearGradient

class TickCheckBox(QCheckBox):
    def paintEvent(self, event):
        super().paintEvent(event)
        
        if self.isChecked():
            p = QPainter(self)
            p.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            opt = QStyleOptionButton()
            self.initStyleOption(opt)
            rect = self.style().subElementRect(QStyle.SubElement.SE_CheckBoxIndicator, opt, self)
            
            p.setPen(QPen(QColor("white"), 2.5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            path = QPainterPath()
            
            path.moveTo(rect.left() + rect.width() * 0.25, rect.top() + rect.height() * 0.5)
            path.lineTo(rect.left() + rect.width() * 0.45, rect.top() + rect.height() * 0.7)
            path.lineTo(rect.left() + rect.width() * 0.75, rect.top() + rect.height() * 0.3)
            p.drawPath(path)
            p.end()

class PremiumLineChart(QFrame):
    def __init__(self, title, color_hex, is_hashrate=False):
        super().__init__()
        self.title = title
        self.color = QColor(color_hex)
        self.is_hashrate = is_hashrate
        self.data = []
        self.setMinimumHeight(220)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def update_data(self, value):
        self.data.append(value)
        if len(self.data) > 60:
            self.data.pop(0)
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w, h = self.width(), self.height()
        
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor("#282a36"))
        p.drawRoundedRect(0, 0, w, h, 10, 10)
        
        p.setPen(QColor("#f8f8f2"))
        font = p.font()
        font.setBold(True)
        p.setFont(font)
        p.drawText(15, 25, self.title)
        
        if len(self.data) < 2:
            p.setPen(QColor("#6272a4"))
            p.drawText(15, h // 2, "Waiting for miner data...")
            return
            
        max_val = max(self.data)
        min_val = min(self.data)
        range_val = max_val - min_val if max_val != min_val else 1
            
        pad_top, pad_bottom = 50, 20
        draw_h = h - pad_top - pad_bottom
        dx = w / (len(self.data) - 1)
        
        path = QPainterPath()
        pts = []
        for i, val in enumerate(self.data):
            x = i * dx
            y = pad_top + draw_h - ((val - min_val) / range_val) * draw_h
            pts.append((x, y))
            
        path.moveTo(pts[0][0], pts[0][1])
        for x, y in pts[1:]:
            path.lineTo(x, y)
            
        p.setPen(QPen(self.color, 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        p.drawPath(path)
        
        path.lineTo(w, h)
        path.lineTo(0, h)
        path.closeSubpath()
        
        grad = QLinearGradient(0, pad_top, 0, h)
        c = QColor(self.color)
        c.setAlpha(80)
        grad.setColorAt(0, c)
        c.setAlpha(0)
        grad.setColorAt(1, c)
        
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(grad)
        p.drawPath(path)
        
        latest_val = self.data[-1]
        
        if self.is_hashrate:
            units = ['H/s', 'kH/s', 'MH/s']
            idx = 0
            display_val = latest_val
            while display_val >= 1000.0 and idx < len(units) - 1:
                display_val /= 1000.0
                idx += 1
            latest_text = f"Latest: {display_val:.2f} {units[idx]}"
        else:
            latest_text = f"Latest: {latest_val:.8f} XMR"
            
        p.setPen(self.color)
        p.drawText(w - 150, 25, latest_text)