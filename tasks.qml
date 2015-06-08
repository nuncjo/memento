import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3
import QtGraphicalEffects 1.0

 Rectangle {
     signal doneClicked(int taskId)
     signal moreClicked(int taskId)
     
   Gradient {
        id:aGradient
        GradientStop { position: 0.5; color: "#e65245" }
        GradientStop { position: 1.0; color: "#e43a15" }
    }
    Gradient {
        id:bGradient
        GradientStop { position: 0.5; color: "#ffb347" }
        GradientStop { position: 1.0; color: "#ffcc33" }
    }
     Gradient {
        id:cGradient
        GradientStop { position: 0.5; color: "#87DA55" }
        GradientStop { position: 1.0; color: "#5ABB38" }
    }          
 
    
     id: mainRectangle;
     objectName: "mainRectangle";
     width: parent.width;
     height: parent.height; 
     color: "#2c3e50"

        Flickable {
            anchors.fill: parent;
            contentHeight: sidebarGrid.height;
            contentWidth: sidebarGrid.width;
            
             Grid {
                 x: 5;
                 y: 5;
                 rows: context.Count;
                 columns: 2;
                 spacing: 10;
                 objectName: "sidebarView";
                 id: sidebarGrid;
                 flow: Grid.TopToBottom;
            
                 Repeater { model: context.Count
                            
                            Rectangle {
                                        width: mainRectangle.width - 10 
                                        height: mainRectangle.height*0.13
                                        
                                        Rectangle {
                                        
                                            property var priority :  context.Tasks[index].priority
                                            
                                            id: priorityRect
                                            width: parent.width*0.15
                                            height: parent.height
                                            
                                            color: {                                 
                                                if(priority == "A"){
                                                    return "#c0392b"
                                                }
                                                if(priority == "B"){
                                                    return "#f1c40f"
                                                }
                                                if(priority == "C"){
                                                    return "#27ae60"
                                                }
                                                
                                                else {
                                                    return "#27ae60"
                                                }
                                            }
                                                                                   
                                        
                                            Text {
                                               id:priorityText
                                               text: {
                                               if (context.Tasks[index].expired == true){
                                                   return context.Tasks[index].priority+"!"
                                               }
                                               else{
                                                   return context.Tasks[index].priority
                                               }
                                               }
                                               font.pointSize: 30
                                               color: "white"
                                               anchors.centerIn: parent
                                               }
                                                                                 
                                                                                           
                                        }
                                        Rectangle {
                                            width: parent.width-priorityRect.width
                                            height: parent.height*0.5
                                            color: "#2980b9"
                                            anchors.top: parent.top
                                            anchors.right: parent.right
                                            
                                            Text { text: context.Tasks[index].message
                                               //font.pointSize: 12
                                               font.pixelSize: Math.round(parent.height / 2.5)
                                               width:parent.width - parent.width * 0.10

                                               color: "#ecf0f1"
                                               clip:true
                                               elide: Text.ElideRight
                                               anchors.centerIn: parent }
                                           
                                        }
                                        
                                       Rectangle {
                                            width: parent.width-priorityRect.width
                                            height: parent.height*0.5
                                            color: "#5F7EAA"
                                            anchors.bottom: parent.bottom
                                            anchors.right: parent.right
                                            
                                             Rectangle {                                                
                                                width: parent.width *0.5
                                                height: parent.height
                                                color: "#446CB3"
                                                anchors.bottom: parent.bottom
                                                anchors.left: parent.left

                                                Rectangle {
                                                    width: parent.width / 2
                                                    height: parent.height
                                                    color: "#446CB3"
                                                    anchors.left: parent.left
                                                    Image {
                                                           id:clockImage
                                                           width: parent.height -6
                                                           height: parent.height -6
                                                           verticalAlignment: parent.AlignVCenter
                                                           source: "icons/png/clock.png"
                                                           fillMode: Image.PreserveAspectFit
                                                           anchors.centerIn: parent
                                                           clip: true
                                                       }
                                                   }

                                                Rectangle {
                                                    width: parent.width / 2
                                                    height: parent.height
                                                    color: "#446CB3"
                                                    anchors.right: parent.right
                                                    Text { text: context.Tasks[index].hour_minute
                                                        font.pointSize: 12
                                                        font.pixelSize: Math.round(parent.height / 2)
                                                        color: "#ecf0f1"
                                                        anchors.centerIn: parent }
                                                    }

                                             }
                                             
                                             Rectangle {
                                                id: doneRectangle
                                                width: parent.width *0.5
                                                height: parent.height
                                                color: "#446CB3"
                                                anchors.bottom: parent.bottom
                                                anchors.right: parent.right
                                                
                                                Button {
                                                     property var taskId :  context.Tasks[index].id
                                                     
                                                     id: checkDoneButton
                                                     width: parent.width  *0.5 - 1
                                                     height: parent.height
                                                     anchors.right: parent.right
                                                    
                                                     style: ButtonStyle {
                                                        background: Rectangle {
                                                            color: control.hovered? "#67809F" : "#27ae60"
                                                          
                                                            Behavior on color {
                                                            ColorAnimation{ 
                                                                duration: 400
                                                                easing.type: Easing.InOutQuad
                                                            }
                                                        }
                                                            
                                                            Text { text: "Done"
                                                               
                                                                font.pixelSize: Math.round(parent.height / 2.5)
                                                                color: "#ecf0f1"
                                                                anchors.centerIn: parent } 
                                                           }
                                                           
                                                     }
                                                     onClicked: {
                                                        mainRectangle.doneClicked(taskId)
                                                     } 
                                                        
                                                 }
                                                
                                                 Button {
                                                     property var taskId :  context.Tasks[index].id
                                                     
                                                     id: moreInfoButton
                                                     width: parent.width  *0.5 - 1
                                                     height: parent.height
                                                     anchors.rightMargin:2
                                                     anchors.left: parent.left
                                                    
                                                     style: ButtonStyle {
                                                        background: Rectangle {
                                                            color: control.hovered? "#67809F" : "#8e44ad"
                                                            Behavior on color {
                                                            ColorAnimation{ 
                                                                duration: 400
                                                                easing.type: Easing.InOutQuad
                                                            }
                                                        }
                                                        
                                                            Text { text: "More"
                                                                font.pixelSize: Math.round(parent.height / 2.5)
                                                                color: "#ecf0f1"
                                                                anchors.centerIn: parent } 
                                                           }
                                                     }
                                                     onClicked: {
                                                        mainRectangle.moreClicked(taskId)
                                                     } 
                                                        
                                                 }                                      
                                            }   
                                            
                                        }

                                        
                            }
                                                                 
                 }
                
             }
        }
 }
