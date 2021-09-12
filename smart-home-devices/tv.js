const { Samsung, KEYS, APPS } = require("samsung-tv-control");

const config = {
  debug: true, // Default: false
  ip: "192.168.0.171",
  mac: "123456789ABC",
  nameApp: "NodeJS-Test", // Default: NodeJS
  port: 8002, // Default: 8002
  token: "12345678",
};

const control = new Samsung(config);
function openYouTube() {
  control.turnOn();
  control
    .isAvailable()
    .then(() => {
      // Get token for API
      control.getToken((token) => {
        console.info("# Response getToken:", token);
      });

      // Send key to TV
      control.sendKey(KEYS.KEY_HOME, function (err, res) {
        if (err) {
          throw new Error(err);
        } else {
          console.log(res);
        }
      });

      // Get all installed apps from TV
      control.getAppsFromTV((err, res) => {
        if (!err) {
          console.log("# Response getAppsFromTV", res);
        }
      });

      // Get app icon by iconPath which you can get from getAppsFromTV
      control.getAppIcon(
        `/opt/share/webappservice/apps_icon/FirstScreen/${APPS.YouTube}/250x250.png`,
        (err, res) => {
          if (!err) {
            console.log("# Response getAppIcon", res);
          }
        }
      );

      // Open app by appId which you can get from getAppsFromTV
      control.openApp(APPS.YouTube, (err, res) => {
        if (!err) {
          console.log("# Response openApp", res);
        }
      });

      // Control will keep connection for next messages in 1 minute
      // If you would like to close it immediately, you can use `closeConnection()`
      control.closeConnection();
    })
    .catch((e) => console.error(e));
}
// get register
registerMsg = {
  outputs: [
    {
      name: "Power on/off",
      description: "",
      isBinary: true,
      outputId: 0,
    },
    {
      name: "You Tube",
      description: "",
      isBinary: false,
      outputId: 1,
    },
    {
      name: "Netflix",
      description: "",
      isBinary: false,
      outputId: 2,
    },
    {
      name: "Volum up",
      description: "",
      isBinary: false,
      outputId: 3,
    },
    {
      name: "Volum down",
      description: "",
      isBinary: false,
      outputId: 4,
    },
    {
      name: "HBO GO",
      description: "",
      isBinary: false,
      outputId: 5,
    },
  ],
  inputs: [],
};

var express = require("express");
var app = express();

app.get("/register", function (req, res) {
  res.send(JSON.stringify(registerMsg));
});

app.post("/output/1", function (req, res) {
  openYouTube();
  res.send("POST Request");
});

var server = app.listen(5000, function () {
  console.log("Node server is running..");
});
