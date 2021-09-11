// const WebSocket = require("ws");
// const exec = require("child_process").exec;
// const base64Encode = function (string) {
//   return new Buffer(string).toString("base64");
// };

// function MySamsungTvRemote(config) {
//   if (!config.ip) {
//     throw new Error("TV IP address is required");
//   }
//   config.name = config.name || "SamsungTvRemote";
//   config.mac = config.mac || "00:00:00:00";
//   config.port = config.port || 8001;
//   config.timeout = config.timeout || 5000;

//   this.sendKey = function (key) {
//     if (key) {
//       const url = `http://${config.ip}:${config.port}/api/v2/channels/samsung.remote.control`;
//       let ws = new WebSocket(url, (error) => {
//         console.log(new Error(error));
//       });
//       ws.on("error", (error) => {
//         console.log(`Samsung Remote Client:${error}`);
//       });
//       ws.on("message", (data, flags) => {
//         data = JSON.parse(data);
//         console.log(data);
//         if (data.event === "ms.channel.connect") {
//           ws.send(
//             JSON.stringify({
//               method: "ms.remote.control",
//               params: {
//                 Cmd: "Click",
//                 DataOfCmd: key,
//                 Option: "false",
//                 TypeOfRemote: "SendRemoteKey",
//               },
//             })
//           );
//           setTimeout(() => {
//             ws.close();
//           }, 1000);
//         }
//       });
//     }
//   };

//   this.isTvAlive = function (done) {
//     return exec("ping -c 1 " + config.ip, (error, stdout, stderr) => {
//       done(error ? false : true);
//     });
//   };
// }
// // const SamsungTvRemote = require("samsung-tv-remote");
// let remote = new MySamsungTvRemote({
//   ip: "192.168.0.171", // required : IP address of the Samsung SmartTV
//   mac: "64:1c:ae:47:bc:83",
//   port: 8001,
//   timeout: 0,
//   name: "Samsung TV",
// });
// remote.isTvAlive(() => {
//   console.log("alive");
//   remote.sendKey("KEY_VOLUP");
// });

// const SamsungRemote = require("samsung-remote");
// const remote = new SamsungRemote({
//   ip: "192.168.0.171", // required: IP address of your Samsung Smart TV
// });
// remote.send("KEY_VOLUP", (err) => {
//   if (err) {
//     throw new Error(err);
//   } else {
//     console.log("f");
//     // command has been successfully transmitted to your tv
//   }
// });

// // check if TV is alive (ping)
// remote.isAlive((err) => {
//   if (err) {
//     throw new Error("TV is offline");
//   } else {
//     console.log("TV is ALIVE!");
//     remote.send("KEY_VOLUP");
//   }
// });

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
