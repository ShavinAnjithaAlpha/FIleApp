
style_sheet = """
            
            QWidget#folder-base {
                    background-color : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0 rgba(0, 0, 10, 0.5), stop : 1.0 rgba(0, 0, 50, 0.5));
                    color : white;
                    font-weight : 400;
                   border-bottom : 1px solid gray;
                    border-radius : 5px;}
                    
            QWidget#folder-base:hover {background : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0 rgb(5, 5, 45), stop : 1.0 rgb(10, 10, 70))}
                    
            QLabel {
                background : none;
                font-weight : 400;}
                
            QLabel#name-label {font-size : 30px;
                            font-family : Helvetica;
                            font-weight : normal;}
                            
            QLabel#time-label {color : rgb(200, 200, 200);
                                font-size : 18px;
                                font-style : italy;
                                }
                                
            QPushButton#fav-button {background : none;
                                    padding : 0px;
                                    margin : 5px;}
            
            """