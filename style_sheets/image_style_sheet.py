style_sheet = """
            
            QWidget {background : none;
                        margin : 0px;}
                        
            QLabel {background : none;}
                        
            QWidget#image-base {background : none;
                                border : 1px solid rgba(60, 60, 60, 0.7);
                                border-radius: 7px;
                                margin : 0px}
                                
            QWidget#image-base:hover {border : 1px solid rgb(80, 80, 80);}
            
            QWidget#selected-image-base {background-color : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0 rgba(15, 0, 40, 0.5), stop : 1.0 rgba(50, 0, 100, 0.5));
                                        border : none;}
                                        
            QWidget#selected-image-base:hover {background-color : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0 rgba(30, 0, 60, 0.5), stop : 1.0 rgba(70, 0, 120, 0.5));
                                        border : none;}
                                        
            QLabel#image-title-label {color : white;
                                        font-size : 20px;}
                        
            QPushButton#fav-button {background : none;
                                    padding : none;}
                                    
            QLabel#image-title-label {font-style : italic;
                                        color : rgb(200, 200, 200);
                                        font-size : 17px;}
        
 """