const { login } = require("tplink-cloud-api");
const uuidV4 = require("uuid/v4");
 
const TPLINK_USER = "srajan.garg@gmail.com";
const TPLINK_PASS = "modernwarfare2";
const TPLINK_TERM = uuidV4();
 
async function main() {
  // log in to cloud, return a connected tplink object
  const tplink = await login(TPLINK_USER, TPLINK_PASS, TPLINK_TERM);
  // get a list of raw json objects (must be invoked before .get* works)
  const dl = await tplink.getDeviceList();
 
  let myPlug = tplink.getHS100("switch1");
  // console.log("deviceId=", myPlug.getDeviceId());
  let response = await myPlug.powerOff();
}
 
main();