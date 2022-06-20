
style_sheet = """

            QWidget {
                background-color : rgb(23, 23, 23);
                padding : 10px;
                color : rgba(250, 250, 250, 0.87);
                font-family : Calibri;
                font-size : 22px;
                font-weight : 300}
                
            QPushButton {
                    background-color : #FF5A00;
                    color : black;
                    font-size : 25px;
                    padding : 7px 8px;
                    margin : 10px;
                    border-radius : 6px;}
                    
            QPushButton:hover {
                    background-color :#EA854E;
                    border-radius : 7px;}
                    
            QLabel {
                color : rgba(250, 250, 250, 0.87);
                font-size : 22px;
                font-family : Calibri;
                margin : 10px;}
                
            QDockWidget {
                border : 5px solid orange;
                titlebar-close-icon : url(img/sys/clear.png);
                titlebar-normal-icon : url(img/sys/uncchecked_box.png);}    
            
            QDockWidget .QWidget {border-right : 1px solid rgb(100, 100, 100);
                                border-radius :5px;}
                
            QDockWidget::title {
                    background-color : rgb(10, 10, 10);
                    border-top-right-radius : 10px;
                    border-top-left-radius : 10px;
                    padding : 10px;}
                
            QScrollArea {
                    background-color : rgb(20, 20, 20);
                    border : none;
                    margin : 0px;}
                    
            QTabBar::tab {background : rgb(70,70, 70);
                        border : none;
                        padding : 5px 30px;
                        border-radius : 10px;
                        min-width : 100px;
                        margin-right : 5px;
                        max-height : 30px;}
                                                
            QTabBar::tab:hover {background-color : rgb(50, 50, 50)}
                
            QTabBar::tab:selected {background-color : rgb(240, 70, 5);
                                    color : black}
                                    
            QTabWidget::pane {border : none;}
            
            QTabBar::close-button {
                        image : url(img/sys/cross-free-icon-font (1).png);
                        sub-control-position : left;
                        margin-right : 10px;}
            
            QScrollBar:vertical {background-color : rgb(20, 20 ,20);
                                                max-width : 10px;
                                                border-radius : 4px}
            QScrollBar::handle:vertical {background-color : rgb(50, 50 ,50);
                                                border-radius : 5px;
                                                margin-top : 0px;
                                                margin-bottom : 0px}

            QScrollBar:horizontal {background-color : rgb(20, 20 ,20);
                                                max-width : 10px;
                                                border-radius : 4px}
            QScrollBar::handle:horizontal {background-color : rgb(50, 50 ,50);
                                                border-radius : 5px;
                                                margin-left : 0px;
                                                margin-right : 0px}                           

            QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover  
                                                        {background-color : rgb(0, 120, 240);
                                                        width : 16px}
            QScrollBar:vertical:hover, QScrollBar:horizontal:hover {min-width : 16px}
            QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical,
            QScrollBar::sub-line:horizontal, QScrollBar::add-line:horizontal 
                                                        {background : none;
                                                        border : none}
            QScrollBar::up-arrow:vertical , QScrollBar::down-arrow:vertical,
            QScrollBar::left-arrow:horizontal , QScrollBar::right-arrow:horizontal
                                                {background : none;
                                                border : none}
                                                
            QToolBar {
                    background-color : rgb(10, 10, 15);
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
                    
            
            
            
            QHeaderView::section {
                background-color: rgba(60, 60, 60, 0.5);
                color: white;
                font-size : 16px;
                padding: 6px;
                border-right: 1px solid #6c6c6c;
            }
            
            QHeaderView::section:checked
            {
                background-color: red;
            }
            
            QHeaderView::section:hover {
                    background-color : rgb(70, 70, 70);
            }
            
            /* style the sort indicator */
            QHeaderView::down-arrow {
                image: url(img/sys/up_arrow.png);
            }
            
            QHeaderView::up-arrow {
                image: url(img/sys/up_arrow.png);
            }
            
            
            QMenuBar {
                background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 lightgray, stop:1 darkgray);
                spacing: 3px; /* spacing between menu bar items */
            }
            
            QMenu {
                background-color : rgba(20, 20, 20, 0.5);
                border-radius : 20px;
                padding : 10px;
            }
            
            QMenu::panel {border-radius : 15px;}
               
            QMenu::item {
                    background-color : rgba(20, 20, 20, 0.5);
                    border-radius : 2px;
                    margin : 0px;
                    padding : 10px 10px 10px 10px;
                    min-width : 250px;
                    font-size : 20px;}
                    
            QMenu::icon {margin : 10px;}
                    
            QMenu::item::selected {
                    background-color : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0.0 rgb(40, 40, 40), stop : 1.0 rgb(60, 60, 60) );
                    color : white;
                  
             }
             
            QMenu::separator {
                height: 2px;
                background: rgba(70, 70, 70, 0.5);
                margin-left: 0px;
                margin-right: 0px;
            }
            
            QMenu::indicator {
                width: 13px;
                height: 13px;
            }
            
            
            
            QTreeView {
                show-decoration-selected: 1;
                border : none;
                border-top : 1px solid rgba(50, 50, 50, 0.5);
                font-size : 20px;
            }
            
            QTreeView::item {
                padding : 3px 5px;
                border-top-color: transparent;
                border-bottom-color: transparent;
            }
            
            QTreeView::item:hover {
                background: rgba(70, 70, 70, 0.5);
                border: 1px solid rgba(80, 80, 80, 0.5);
            }
            
            QTreeView::item:selected {
                background-color : rgba(220, 0, 250, 0.6);
                border: 1px solid rgba(80, 80, 80, 0.5);
            }
            
            QTreeView::item:selected:active{
                background-color : rgba(20, 100, 200, 0.6);
            }
            
            QTreeView::item:selected:!active {
                background: rgba(50, 50, 50, 0.5);
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
                                    
            QComboBox QAbstractItemView {background-color  : rgb(70, 70, 70);
                                        padding : 10px;
                                        item-spacing : 10px;
                                        border-bottom-left-radius : 7px;
                                        border-bottom-right-radius : 7px;}
             
           
            
            
            
            
            QLineEdit {padding : 10px 15px;
                        background-color : rgb(60, 60, 60);
                        border-radius : 8px;
                        border : 0.5px solid rgb(220, 50, 10);
                        font-size : 22px;
                        color  : white}
                        
            QLineEdit:focus {border-radius : 8px;
                    border : none;
                    border-left : 3px solid rgb(240, 50 , 5);
                    border-radius : 0px;
                    }            
                    
            
            
            
            QInputDialog QPushButton {
                            width : 130px;
                            padding : 7px;
                            font-size : 18px;}
                            
            QSeparator {background-color : white;
                        border-color : white;
                        border-width : 5px;
                        width : 3px;}
                        
            
            QPushButton#action-button {background : none;
                                    margin : 10px;
                                    padding : 7px;
                                    color : white;
                                    max-width : 150px;}
                                    
            QPushButton#action-button:hover {background-color : rgba(50, 50, 50, 0.5);
                                            border-radius : 7px;}
                                            
            QToolBar#file-area-tool-bar {background : none;
                                        border : 2px solid rgb(120, 120, 120);
                                        border-left : 2px solid rgb(120, 120, 120);
                                        border-radius : 7px;}
                            
            QLineEdit#search-bar {background-color : rgb(60, 60, 60);
                                    padding : 5px 10px;
                                    font-size  : 20px;
                                    border-radius : 8px;
                                    border : none;}
            
            QLineEdit#search-bar:focus , QLineEdit#search-bar:hover {
                background-color : rgb(70, 70, 70);
                border : 1px solid rgb(100, 100, 100);
            
            }
                                    
            
            QGroupBox {
                border: 0.5px solid rgb(70, 70, 70);
                border-radius: 8px;
                font-size : 18px;
                margin : 10px 5px; /* leave space at the top for the title */
            }
                                    
            QPushButton#action_button {background : none;
                                        border : none;
                                        font-size : 18px;
                                        text-align : align-bottom;
                                        color : white;
                                        margin : 5px;}
                                        
            QPushButton#action_button:hover {background-color  :rgba(70, 70, 70, 0.5);
                                            border-radius : 8px;
                                            }
                                            
            QPushButton#search-bar-button {
                    background : none;
                    color : white;
                    padding : 12px;}
            QPushButton#search-bar-button:hover {background-color : rgba(50, 50, 50, 0.5)}    
                        
            QMessageBox {min-width : 500px;}
            
            QMessageBox QPushButton {min-width : 65px;}
            QMessageBox QLabel {color : rgba(255, 255, 255, 0.80);
                                font-size : 21px;}
            
            QToolBar::handle {
                    border-color : red;
                    image: url(img/sys/menu-dots-vertical-free-icon-font.png);
                    width : 30px;
                    height : 40px;
                }
                
            QComboBox#sort-box {border : 1px solid rgba(255, 255, 255, 0.3);
                                border-radius : 5px;
                                background-color : rgb(25, 25, 25);}
            QComboBox#sort-box2 {border : 0px solid rgba(255, 255, 255, 0.3);
                                border-radius : 5px;
                                background-color : rgb(25, 25, 25);}
                                
            
                    
            QPushButton#hide-button {
                    background : none;
                    border-radius : 8px;
                    padding : 8px;
                }
                
            QPushButton#hide-button:hover {
                    background-color : rgba(50, 50, 50, 0.8)}
            
            """