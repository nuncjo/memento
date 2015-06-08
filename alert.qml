import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Controls.Styles 1.3
import QtGraphicalEffects 1.0

Rectangle {
            signal doneClicked(int taskId)
            signal cancelClicked(int taskId)
            anchors.centerIn: parent
            width: parent.width
            height: parent.height
            id: mainRectangle;
            objectName: "mainRectangle";

            Rectangle {

                property var priority :  context.Task.priority
                id: priorityRect
                width: parent.width*0.15
                height: parent.height
                //color: mouseArea.containsMouse ? "#682244" : "#D5BC7C"
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
                
                Text { text: context.Task.priority
                   font.pointSize: 30
                   anchors.centerIn: parent }

            }
            Rectangle {
                width: parent.width-priorityRect.width
                height: parent.height*0.5
                color: "#2980b9"
                anchors.top: parent.top
                anchors.right: parent.right

                Text { text: context.Task.message

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
                        Text { text: context.Task.hour_minute
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
                         property var taskId :  context.Task.id

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

                                Text { text: "Set done"
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
                         property var taskId :  context.Task.id

                         id: cancelButton
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

                                Text { text: "Delay 30 min"
                                    font.pixelSize: Math.round(parent.height / 2.5)
                                    color: "#ecf0f1"
                                    anchors.centerIn: parent }
                               }
                         }
                         onClicked: {
                            mainRectangle.cancelClicked(taskId)
                         }

                     }
                }

            }

}
