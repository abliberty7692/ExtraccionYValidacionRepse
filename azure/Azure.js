const { containerServicios, downloadBlobToFile } = require("./config/config");


const downloadFile = async(nameFile, downloadPath )=>{
    try {
        console.log("Downloading "+nameFile+"...")
        await downloadBlobToFile(containerServicios,nameFile,`${downloadPath}/${nameFile}`);
    } catch(err) {
        console.log(err);
    }
}

module.exports = downloadFile;