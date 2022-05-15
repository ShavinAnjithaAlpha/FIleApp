
style_sheet = """
            
            QWidget#folder-base {
                    background : none;
                    color : white;
                    font-weight : 400;
                   border-bottom : 1px solid rgba(60, 60, 60, 0.7);
                    border-radius : 5px;}
                    
            QWidget#selected-folder-base {
                background-color : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0 rgba(15, 0, 40, 0.5), stop : 1.0 rgba(50, 0, 100, 0.5));
                color : white;
                border-radius : 5px;}
                    
            QWidget#folder-base:hover {border : 1px solid rgb(80, 80, 80);
                                        border-right : 1px solid rgb(80, 80, 80);}
                    
            QWidget#selected-folder-base:hover {background : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0 rgb(20, 5, 45), stop : 1.0 rgb(40, 10, 70))}
                    
            QLabel {
                background : none;
                font-weight : 400;}
                
            QLabel#name-label {font-size : 28px;
                            font-family : Calibri;
                            font-weight : normal;}
                            
            QLabel#time-label {color : rgb(150, 150, 150);
                                font-size : 20px;
                                font-style : italic;
                                }
                                
            QPushButton#fav-button {background : none;
                                    padding : 0px;
                                    margin : 5px;}
            
            """