
style_sheet = """
            
            QWidget {
                background-color : rgb(25, 25, 25);
                padding : 10px;
                color : rgb(220, 220, 220);
                font-family : Helvetica;
                font-size : 22px;
                font-weight : 300}
                
            QPushButton {
                    background-color : rgb(220, 70, 10);
                    color : black;
                    font-size : 25px;
                    padding : 7px 8px;
                    margin : 10px;
                    border-radius : 5px;}
                    
            QPushButton:hover {
                    background-color : rgb(250, 50, 0);
                    border-radius : 7px;}
                    
            QLabel {
                color : rgb(220, 220, 220);
                font-size : 22px;
                font-family : Helvetica;
                margin : 10px;}
                
            QDockWidget {
                border : 5px solid orange;
                titlebar-close-icon : url(img/sys/clear.png);
                titlebar-normal-icon : url(img/sys/uncchecked_box.png);}    
            
            QDockWidget QWidget {background : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0 rgb(215, 15, 15), stop : 1.0 rgb(0, 0, 0));}
                
            QDockWidget::title {
                    background-color : rgb(10, 10, 10);
                    border-top-right-radius : 10px;
                    border-top-left-radius : 10px;
                    padding : 10px;}
                
            QScrollArea {
                    background-color : rgb(25, 25, 25);
                    border : none;
                    margin : 0px;}
                    
            QTabBar::tab {background : black;
                        border : none;
                        padding : 10px 30px;
                        border-top-right-radius : 10px;
                        border-top-left-radius : 10px;}
                                                
            QTabBar::tab:hover {background-color : rgb(20, 20, 20)}
                
            QTabBar::tab:selected {background-color : rgb(240, 70, 5);
                                    color : black}
                                    
            QTabWidget::pane {border : none;}
            
            QTabBar::close-button {
                        image : url(img/sys/remove.png);
                        sub-control-position : left}
            
            QScrollBar:vertical, QScrollBar:horizontal {background-color : rgb(20, 20 ,20);
                                                max-width : 10px;
                                                border-radius : 5px}
            QScrollBar::handle:vertical {background-color : rgb(50, 50 ,50);
                                                border-radius : 5px;
                                                margin-top : 0px;
                                                margin-bottom : 0px}
                                                
            QScrollBar::handle:horizontal {background-color : rgb(50, 50 ,50);
                                                border-radius : 5px;
                                                margin-left : 0px;
                                                margin-right : 0px}
                                                
            QScrollBar::handle:vertical:hover {background-color : rgb(0, 120, 240)}
                
            QScrollBar::handle:horizontal:hover {background-color  :rgb(0, 120, 240)}
                
            QScrollBar::sub-line:horizontal, QScrollBar::add-line:horizontal 
                                                        {background : none;
                                                        border : none}
                                                        
            QScrollBar::sub-line:horizontal, QScrollBar::add-line:horizontal {background : none;
                                                        border : none}
                
            QScrollBar::up-arrow:vertical , QScrollBar::down-arrow:vertical
                                                {background : none;
                                                border : none}
                                                
            QScrollBar::right-arrow:horizontal , QScrollBar::left-arrow:horizontal
                                                {background : none;
                                                border : none}
                                                
            QToolBar {
                    background-color : rgb(15, 15, 15);
                    padding : 15px;
                    margin-bottom : 10px;}
                    
            QToolBar QToolButton {
                    background : none;
                    margin : 5px;
                    padding : 20px;
                    border-radius : 12px;
                    font-size : 18px;}
                    
            QToolBar QToolButton:hover {
                    background-color: rgb(40, 40, 40);}
            
            QMenu {
                border-radius : 20px;
                padding : 10px;
            }
            
            QMenu::panel {border-radius : 15px;}
               
            QMenu::item {
                    border-radius : 2px;
                    margin : 0px;
                    padding : 10px;
                    min-width : 250px;
                    font-size : 20px;}
                    
            QMenu QIcon {margin : 10px;}
                    
            QMenu::item::selected {
                    background-color : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0.0 rgb(40, 40, 40), stop : 1.0 rgb(60, 60, 60) );
                    color : white;
                    border-bottom : 1px solid rgb(100, 100, 100);
                    padding : 10px;
             }
             
             QComboBox {font-size : 18px;
                        background-color : rgb(40, 40, 40);
                        padding : 12px;
                        border-radius : 5px}
             
             QComboBox:item {padding : 15px;}
             
             QComboBox::drop-down {border-radius :12px;
                                    padding : 8px;
                                    subcontrol-origin: padding;
                                    subcontrol-position: top right;}
             
             QComboBox QAbstractItemView::item {
                                selection-background-color: rgb(50, 50, 50);
                                padding : 15px;
                                background-color : rgba(60, 60,60, 0.5)}
                        
            
            QLineEdit {padding : 10px 15px;
                        background-color : rgb(60, 60, 60);
                        border-radius : 8px;
                        font-size : 20px;
                        color  : white}
                        
            QLineEdit:focus {border-bottom : 3px solid rgb(240, 50 , 5)}            
                    
            QInputDialog QPushButton {
                            width : 130px;
                            padding : 7px;
                            font-size : 18px;}
                            
            QSeparator {background-color : white;
                        border-color : white;
                        width : 3px;}
                            
             
        
            """