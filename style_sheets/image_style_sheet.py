style_sheet = """
            
            QWidget {background : none;
                        margin : 0px;}
                        
            QLabel {background : none;}
                        
            QWidget#image-base {background : none;
                                border : 1px solid rgba(60, 60, 60, 0.7);
                                border-radius: 7px;
                                margin : 0px;
                                padding : 10px;}
                                
            QWidget#image-base:hover {border : 1px solid rgb(80, 80, 80);}
            
            QWidget#selected-image-base {background-color : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0 rgba(50, 0, 70, 0.7), stop : 1.0 rgba(100, 0, 120, 0.7));
                                        border : none;
                                        padding : 10px;}
                                        
            QWidget#selected-image-base:hover {background-color : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0 rgba(70, 0, 80, 0.5), stop : 1.0 rgba(100, 0, 130, 0.5));
                                        border : none;}
                                        
            QLabel#name-label {color : rgb(220, 220, 220);
                                        font-size : 25px;
                                        font-family : Calibri;}
                        
            QPushButton#fav-button {background : none;
                                    padding : 15px;
                                    margin : 10px;}
                                    
            QLabel#time-label {font-style : italic;
                                        color : rgb(150, 150, 150);
                                        font-size : 20px;}
                                        
            QLabel#size-label {color : rgb(180, 180, 180);
                                font-size : 22px;}
        
 """