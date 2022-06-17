
style_sheet = """
            
            QWidget#folder-base {
                    background : none;
                    color : white;
                    font-weight : 400;
                    border-radius : 5px;}
                    
            QWidget#selected-folder-base {
                background-color : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0.03 rgb(187, 15, 255), stop : 1.0 rgb(5, 49, 255));
                color : white;
                border-radius : 5px;}
                    
            QWidget#folder-base:hover {border : 1px solid rgb(80, 80, 80);
                                        border-right : 1px solid rgb(80, 80, 80);}
                    
            QWidget#selected-folder-base:hover {background : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0.03 rgb(150, 15, 245), stop : 1.0 rgb(10, 50, 255))}
                    
            QLabel {
                background : none;
                font-weight : 400;
                margin : 0px;
                padding : 5px; } 
                
            QLabel#name-label {
                            color : rgba(255, 255, 255, 0.87);
                            font-size : 24px;
                            font-family : Calibri;
                            font-weight : normal;
                            max-height : 30px;}
                            
            QLabel#time-label {color : rgba(250, 250, 250, 0.6);
                                font-size : 20px;
                                font-style : italic;
                                }
                                
            QPushButton#fav-button {background : none;
                                    padding : 0px;
                                    margin : 5px;}
            
            """