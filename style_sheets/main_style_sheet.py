
style_sheet = """
            
            QWidget {
                background-color : rgb(35, 35, 35);
                padding : 10px;
                color : rgb(220, 220, 220);
                font-family : Helvetica;
                font-size : 22px;
                font-weight : 300}
                
            QPushButton {
                    background-color : rgb(250, 50, 0);
                    color : black;
                    font-size : 25px;
                    padding : 7px 8px;
                    margin : 10px;
                    border-radius : 5px;}
                    
            QPushButton:hover {
                    background-color : rgb(240, 70, 0);
                    border-radius : 7px;}
                    
            QLabel {
                color : rgb(220, 220, 220);
                font-size : 22px;
                font-family : Helvetica;
                margin : 10px;}
                
            QDockWidget {
                border : 5px;
                titlebar-close-icon : url(img/sys/close.png);
                titlebar-normal-icon : url(img/sys/uncchecked_box.png);}    
                
            QScrollArea {
                    background-color : rgb(35, 35, 35);
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
            
            QTabBar::tab:close-button {
                        icon : url(img/sys/close.png);}
            
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
        
            """