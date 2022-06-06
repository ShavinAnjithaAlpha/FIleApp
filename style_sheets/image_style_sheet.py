style_sheet = """
            
           
            QWidget {background : none;
                        margin : 0px;}
                        
            QLabel {background : none;}
                        
            QWidget#image-base {background : none;
                                border-radius: 7px;
                                margin : 0px;
                                padding : 10px;}
                                
            QWidget#image-base:hover {border : 1px solid rgb(80, 80, 80);}
            
            QWidget#selected-image-base {background-color : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0 #AC32E4, stop : 0.48 #7918F2, stop : 1.0 #4801FF);
                                        border : none;
                                        padding : 10px;}
                                        
            QWidget#selected-image-base:hover {background-color : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0.11 rgb(193, 98, 253), stop : 0.91 rgb(0, 49, 165));
                                        border : none;}
                                        
            QLabel#name-label {color : rgba(250, 250, 250, 0.87);
                                        font-size : 22px;
                                        font-family : Calibri;}
                        
            QPushButton#fav-button {background : none;
                                    padding : 15px;
                                    margin : 10px;}
                                    
            QLabel#time-label {font-style : italic;
                                        color : rgba(250, 250, 250, 0.6);
                                        font-size : 21px;}
                                        
            QLabel#size-label {color : rgba(250, 250, 250, 0.6);
                                font-size : 22px;}
        
 """