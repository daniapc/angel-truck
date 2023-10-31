from flask import Flask, request, render_template
app = Flask(__name__, template_folder="html/")

from AngelTruck import AngelTruck
        
@app.route("/")
def home():
    return "Página Inicial"  # return a string

@app.route("/videoanalisys",methods=["GET", "POST", "PUT"])
def video_analisys():
    file = request.files['file']

    file.save("data/video.mp4")

    angel_truck = AngelTruck("video.mp4", 60)
    angel_truck.video_analisys()
    angel_truck.draw_map(800, 600, 7)

    return "Process finished successfuly."

@app.route("/showmap", methods=['GET'])
def show_map():
    encoded = AngelTruck.encode_map('map.png')

    return render_template('map.html', image=encoded)

@app.route("/getmap", methods=['GET'])
def get_map():
    file = open("map.png","rb")

    return file

@app.route("/getvideo", methods=['GET'])
def get_video():
    file = open("output.avi","rb")

    return file
    
# start the server with the "run()" method
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)