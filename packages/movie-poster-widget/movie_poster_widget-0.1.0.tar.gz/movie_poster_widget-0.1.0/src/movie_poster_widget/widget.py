# src/movie_poster_widget/widget.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap


class MoviePosterWidget(QWidget):
    def __init__(self, poster_path, parent=None):
        super(MoviePosterWidget, self).__init__(parent)
        self.poster_path = poster_path
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Image Label
        self.image_label = QLabel(self)
        self.pixmap = QPixmap(self.poster_path)
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.image_label)
        self.setLayout(self.layout)

    def set_poster_size(self, width, movie_poster_frame):
        if width > 840:
            movie_poster_frame.setFixedHeight(200)
            size = QSize(150, 200)
        else:
            movie_poster_frame.setFixedHeight(150)
            size = QSize(80, 150)

        self.image_label.setPixmap(
            self.pixmap.scaled(size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def set_title_size(self, width, movie_title):
        if width > 840:
            movie_title.setFixedWidth(200)
        else:
            movie_title.setFixedWidth(100)

    def add_movies(self, width, movie_index, scroll_area_grid_layout, movie_poster_frame, posters_per_row):
        if width > 840:
            if movie_index % posters_per_row != 0:
                scroll_area_grid_layout.addWidget(
                    movie_poster_frame,
                    (movie_index // posters_per_row) + 1,
                    movie_index % posters_per_row,
                    1,
                    1,
                    Qt.AlignmentFlag.AlignLeft,
                )
            else:
                scroll_area_grid_layout.addWidget(
                    movie_poster_frame, (movie_index // posters_per_row), posters_per_row, 1, 1, Qt.AlignmentFlag.AlignLeft
                )
        else:
            if movie_index % (posters_per_row-1) != 0:
                scroll_area_grid_layout.addWidget(
                    movie_poster_frame,
                    (movie_index // (posters_per_row-1)) + 1,
                    movie_index % (posters_per_row-1),
                    1,
                    1,
                    Qt.AlignmentFlag.AlignLeft,
                )
            else:
                scroll_area_grid_layout.addWidget(
                    movie_poster_frame, (movie_index // (posters_per_row-1)), (posters_per_row-1), 1, 1, Qt.AlignmentFlag.AlignLeft
                )
