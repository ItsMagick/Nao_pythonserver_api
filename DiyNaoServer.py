from time import sleep, time
from tokenize import Double
from turtle import speed
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import cgi
from naoqi import ALProxy
from PIL import Image
import time
import base64
from StringIO import StringIO

from io import BytesIO


class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
    def do_HEAD(self):
        self._set_headers()
        
    # GET sends back a Hello world message
    def do_GET(self):
        self._set_headers()
        self.wfile.write(json.dumps({'Bruh': 'You must send a POST message not GET... https://www.youtube.com/watch?v=2ZIpFytCSVc', 'received': 'ok'}))
        
    # Tutorial how to use JSON in python: https://realpython.com/python-json/
    # POST
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400) #Return status codeto indicate wrong client data.
            self.end_headers()
            return
            
        # read the message and convert it into a python dictionary
        length = int(self.headers.getheader('content-length'))
        jsonMessage = json.loads(self.rfile.read(length))
        
        naoIp = ""
        naoPort = 0

        jsonResponse = {
            "messageId": jsonMessage['messageId'],
	        "success": True,
	        "message": '',
	        "data": {},
        }

        try:
            naoIp = str(jsonMessage['naoIp'])
            naoPort =  int(jsonMessage['naoPort'])
        except Exception as e:
            jsonResponse['success'] = False
            jsonResponse['message'] = "Unable to parse NAO ip and port."

            self._set_headers()
            self.wfile.write(json.dumps(jsonResponse))

            return

        print(naoIp)
        print(naoPort)

        # Detect NAO action.
        if 'tts' in jsonMessage['actionId']:
            try:
                tts = ALProxy('ALTextToSpeech', str(naoIp), int(naoPort)) # naoIp + "", naoPort)
                
                message = str(jsonMessage["data"]["text"])
                
                tts.say(message)
            except Exception as e:
                jsonResponse['success'] = False
                jsonResponse['message'] = "Unable to perform action 'tts'. Cause: " + str(e)

                self._set_headers()
                self.wfile.write(json.dumps(jsonResponse))

                return

            self._set_headers()
            self.wfile.write(json.dumps(jsonResponse))

        jsonResponse['success'] = False
        jsonResponse['message'] = "Unable to find the sent action-ID."
        
        self._set_headers()
        self.wfile.write(json.dumps(jsonMessage))



        if "motion" in jsonMessage["actionId"]:
            try:
                motion = ALProxy("ALRobotPosture", str(naoIp), int(naoPort))

                apply = str(jsonMessage["data"]["apply"])
                speed = float(jsonMessage["data"]["speed"])
                motion.goToPosture(apply,speed)


            
            except Exception as e:
                jsonResponse["success"] = False
                jsonResponse["message"] = "Unable to perform action 'motion'. Cause: " + str(e)

                self._set_headers()
                self.wfile.write(json.dumps(jsonResponse))

                return

            self._set_headers()
            self.wfile.write(json.dumps(jsonResponse))

        jsonResponse['success'] = False
        jsonResponse['message'] = "Unable to find the sent action-ID."

        self._set_headers()
        self.wfile.write(json.dumps(jsonMessage))

        #kein nutzen soweit
        if "wakeUp" in jsonMessage["actionId"]:
            try:
                motion = ALProxy("ALMotion", str(naoIp), int(naoPort))

                motion.wakeUp(True)
            
            except Exception as e:
                jsonResponse["success"] = False
                jsonResponse["message"] = "Unable to perform action 'wakeUp'. Cause: " + str(e)

                self._set_headers()
                self.wfile.write(json.dumps(jsonResponse))

                return

            self._set_headers()
            self.wfile.write(json.dumps(jsonResponse))

        jsonResponse['success'] = False
        jsonResponse['message'] = "Unable to find the sent action-ID."

        self._set_headers()
        self.wfile.write(json.dumps(jsonMessage))


        if "rest" in jsonMessage["actionId"]:
            try:
                motion = ALProxy("ALMotion", str(naoIp), int(naoPort))

                motion.rest()
            
            except Exception as e:
                jsonResponse["success"] = False
                jsonResponse["message"] = "Unable to perform action 'motion'. Cause: " + str(e)

                self._set_headers()
                self.wfile.write(json.dumps(jsonResponse))

                return

            self._set_headers()
            self.wfile.write(json.dumps(jsonResponse))

        jsonResponse['success'] = False
        jsonResponse['message'] = "Unable to find the sent action-ID."

        self._set_headers()
        self.wfile.write(json.dumps(jsonMessage))


#########################################################################################################################################################


        if "audioPlayer" in jsonMessage["actionId"]:
            try:
                player = ALProxy("ALAudioPlayer", str(naoIp), int(naoPort))

                player.playFile(str(jsonMessage["data"]["path"]))
                
                #taskId = player.loadFile(str(jsonMessage["data"]["path"]))
                #player.play(taskId)


                #if "pause" in jsonMessage["data"]["state"]:
                    #player.pause(taskId)

                #if "continue" in jsonMessage["data"]["state"]:
                    #player.play(taskId)


            except Exception as e:
                jsonResponse["success"] = False
                jsonResponse["message"] = "Unable to perform action 'audioPlayer'. Cause: " + str(e)

                self._set_headers()
                self.wfile.write(json.dumps(jsonResponse))

                return

            self._set_headers()
            self.wfile.write(json.dumps(jsonResponse))

        jsonResponse['success'] = False
        jsonResponse['message'] = "Unable to find the sent action-ID."

        self._set_headers()
        self.wfile.write(json.dumps(jsonMessage))



        if "setMaxVolume" in jsonMessage["actionId"]:
            try:
                player = ALProxy("ALAudioPlayer", str(naoIp), int(naoPort))

                player.setMasterVolume(float(jsonMessage["data"]["setMaxVolume"]))
            
            except Exception as e:
                jsonResponse["success"] = False
                jsonResponse["message"] = "Unable to perform action 'setMaxVolume'. Cause: " + str(e)

                self._set_headers()
                self.wfile.write(json.dumps(jsonResponse))

                return

            self._set_headers()
            self.wfile.write(json.dumps(jsonResponse))

        jsonResponse['success'] = False
        jsonResponse['message'] = "Unable to find the sent action-ID."

        self._set_headers()
        self.wfile.write(json.dumps(jsonMessage))


        
        if "audioStop" in jsonMessage["actionId"]:
            try:
                player = ALProxy("ALAudioPlayer", str(naoIp), int(naoPort))

                player.stopAll()
            
            except Exception as e:
                jsonResponse["success"] = False
                jsonResponse["message"] = "Unable to perform action 'audioStop'. Cause: " + str(e)

                self._set_headers()
                self.wfile.write(json.dumps(jsonResponse))

                return

            self._set_headers()
            self.wfile.write(json.dumps(jsonResponse))

        jsonResponse['success'] = False
        jsonResponse['message'] = "Unable to find the sent action-ID."

        self._set_headers()
        self.wfile.write(json.dumps(jsonMessage))


        if "audioRecord" in jsonMessage["actionId"]:
            try:
                recorder = ALProxy("ALAudioRecorder", str(naoIp), int(naoPort))
                channels = ALProxy("ALValue", str(naoIp), int(naoPort))

                channels.arrayPush(0)
                channels.arrayPush(0)
                channels.arrayPush(1)
                channels.arrayPush(0)

                recorder.startMicrophonesRecording(str(jsonMessage["data"]["filename"]),str(jsonMessage["data"]["type"],int(jsonMessage["data"]["samplerate"])),channels)

                #sleep(5.0)

                #recorder.stopMicrophonesRecording()
            except Exception as e:
                jsonResponse["success"] = False
                jsonResponse["message"] = "Unable to perform action 'audioRecord'. Cause: " + str(e)

                self._set_headers()
                self.wfile.write(json.dumps(jsonResponse))

                return

            self._set_headers()
            self.wfile.write(json.dumps(jsonResponse))

        jsonResponse['success'] = False
        jsonResponse['message'] = "Unable to find the sent action-ID."

        self._set_headers()
        self.wfile.write(json.dumps(jsonMessage))

#########################################################################################################################################################

        #via get anfrage vom iphone, video von nao bekommen

        if "captureImage" in jsonMessage["actionId"]:
            try:
                camProxy = ALProxy("ALVideoDevice", naoIp, naoPort)
                resolution = int(jsonMessage["data"]["resolutionId"])   # VGA
                colorSpace = 11   # RGB

                videoClient = camProxy.subscribeCamera("python_client", 0, resolution, colorSpace, 5)

                t0 = time.time()

                # Get a camera image.
                # image[6] contains the image data passed as an array of ASCII chars.
                naoImage = camProxy.getImageRemote(videoClient)

                t1 = time.time()

                # Time the image transfer.
                print ("acquisition delay "), t1 - t0

                camProxy.unsubscribe(videoClient)


                # Now we work with the image returned and save it as a PNG  using ImageDraw
                # package.

                # Get the image size and pixel array.
                imageWidth = naoImage[0]
                imageHeight = naoImage[1]
                array = naoImage[6]

                # Create a PIL Image from our pixel array.
                image = Image.frombytes("RGB", (imageWidth, imageHeight), array)

                # Save the image.
                # image.show()

                imageQualityPercentage = int(jsonMessage["data"]["imageQualityPercentage"])

                output = BytesIO()
                image.save(output, format='JPEG', quality= imageQualityPercentage)
                im_data = output.getvalue()
                image_data = base64.b64encode(im_data)
                if not isinstance(image_data, str):
                    # Python 3, decode from bytes to string
                    image_data = image_data.decode()

                #data_url = 'data:image/jpg;base64,' + image_data
                #print(data_url)

                jsonResponse["data"] = {
                    "base64Jpeg" : image_data
                }

            
            except Exception as e:
                jsonResponse["success"] = False
                jsonResponse["message"] = "Unable to perform action 'captureImage'. Cause: " + str(e)

                self._set_headers()
                self.wfile.write(json.dumps(jsonResponse))

                return

            self._set_headers()
            self.wfile.write(json.dumps(jsonResponse))

        jsonResponse['success'] = False
        jsonResponse['message'] = "Unable to find the sent action-ID."

        self._set_headers()
        self.wfile.write(json.dumps(jsonMessage))

########################################################################################################################################


        if "movement" in jsonMessage["actionId"]:
            try:
                motionProxy = ALProxy("ALMotion", naoIp, naoPort)

                StiffnessOn(motionProxy)

                enableArmsInWalkAlgorithm = bool(jsonMessage["data"]["enableArmsInWalkAlgorithm"])


                motionProxy.setWalkArmsEnabled(enableArmsInWalkAlgorithm, enableArmsInWalkAlgorithm)
                motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

                xForwardBackward = float(jsonMessage["data"]["xCoordinate"])
                yLeftRight = float(jsonMessage["data"]["yCoordinate"])
                tRotation = float(jsonMessage["data"]["tCoordinate"])
                speed = float(jsonMessage["data"]["speed"])

                motionProxy.setWalkTargetVelocity(xForwardBackward, yLeftRight, tRotation, speed)
            




            except Exception as e:
                jsonResponse["success"] = False
                jsonResponse["message"] = "Unable to perform action 'movement'. Cause: " + str(e)

                self._set_headers()
                self.wfile.write(json.dumps(jsonResponse))

                return

            self._set_headers()
            self.wfile.write(json.dumps(jsonResponse))

        jsonResponse['success'] = False
        jsonResponse['message'] = "Unable to find the sent action-ID."

        self._set_headers()
        self.wfile.write(json.dumps(jsonMessage))
        
        ####################################################################################
        
        
        if "batteryInfo" in jsonMessage["actionId"]:
            try:
                batteryProxy = ALProxy("ALBatteryProxy", str(naoIp), int(naoPort))

                batteryPercentage = batteryProxy.getBatteryCharge()
            
            except Exception as e:
                jsonResponse["success"] = False
                jsonResponse["message"] = "Unable to perform action 'batteryInfo'. Cause: " + str(e)

                self._set_headers()
                self.wfile.write(json.dumps(jsonResponse))

                return

            self._set_headers()
            self.wfile.write(json.dumps(jsonResponse))

        jsonResponse['success'] = False
        jsonResponse['message'] = "Unable to find the sent action-ID."

        self._set_headers()
        self.wfile.write(json.dumps(jsonMessage))
       
       ####################################################################################
        
        if "language" in jsonMessage["actionId"]:
            try:
                languageProxy = ALProxy("ALDialogProxy", str(naoIp), int(naoPort))

                languageProxy.setLanguage(str(jsonMessage["data"]["language"]))
                # data: "language = "German"
            
            except Exception as e:
                jsonResponse["success"] = False
                jsonResponse["message"] = "Unable to perform action 'motion'. Cause: " + str(e)

                self._set_headers()
                self.wfile.write(json.dumps(jsonResponse))

                return

            self._set_headers()
            self.wfile.write(json.dumps(jsonResponse))

        jsonResponse['success'] = False
        jsonResponse['message'] = "Unable to find the sent action-ID."

        self._set_headers()
        self.wfile.write(json.dumps(jsonMessage))
        
        
      



def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)



def run(server_class=HTTPServer, handler_class=Server, port=8283):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    print ('Starting super hyper cool NAO hack-server on port %d...') % port
    httpd.serve_forever()
    
if __name__ == "__main__":
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
        
