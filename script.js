require('dotenv').config();

const fs = require('fs');
const { leerExcel, convertirBase64 } = require('./controllers/DocumentController.js');
const { crearRutas, descargarBlobs } = require('./functions/AzureFunctions');
const { spawn } = require('child_process');
const parserDoc = require('./STPS/ParserDoc');
const extraerReporte = require('./STPS/STPSReport');
const arrayToCsv = require('./functions/array2csv');

const azureDataFile = leerExcel(`./doc/plantillaDescargas.xlsx`);
const fechaActual = `${ new Date().getDate() }-${ new Date().getMonth() + 1 }-${ new Date().getFullYear() }`;
const pathDownloads = `./download/${ fechaActual }`; 
const csvPath = './ReporteRepse.csv';

//crearRutas(pathDownloads, azureDataFile);
async function main() {
    if(!fs.existsSync(pathDownloads))
        try{
            fs.mkdirSync(pathDownloads);
            console.log(`${pathDownloads} creada con éxito`);
        } catch(err) {
            throw err;
        }
    if(azureDataFile.length > 400) {
        pages = azureDataFile.length/400
        for(i=0; i<=Math.floor(pages); i++) {
            if(i == Math.floor(pages))
                end = azureDataFile.length;
            else
                end = (i+1)*400
            await descargarBlobs(azureDataFile.slice(i*400, end), pathDownloads);
        }
    }
    else
        await descargarBlobs(azureDataFile, pathDownloads);

    console.log("================================");
    const lstRepseFiles = fs.readdirSync(pathDownloads);

    //lstRepseInfo = [["RFC", "REPSE", "RAZON_SOCIAL", "FECHA", "ASUNTO"]];
    lstRepseInfo = [];
        
    for(repse of lstRepseFiles) {
        console.log("================================")
        if(!repse.toLowerCase().includes(".pdf")) continue;
        
        console.log("Extracting "+repse+"...");
        let repseData = await extraerReporte(pathDownloads+"/"+repse);
        console.log(repseData);
        /*lstRepseInfo.push([repseData["rfc"], repseData["repse"], 
                            repseData["razonSocial"], repseData["fecha"],
                            repseData["asunto"]]);*/
        if(repseData === undefined) continue;
        repseKeys = Object.keys(repseData);
        if('rfc' in repseKeys) repseData.rfc ="";
        if('repse' in repseKeys) repseData.repse ="";
        if('razonSocial' in repseKeys) repseData.razonSocial ="";
        if('fecha' in repseKeys) repseData.fecha ="";
        if('asunto' in repseKeys) repseData.asunto ="";
        if('documento' in repseKeys) repseData.documento ="";
        lstRepseInfo.push(repseData)
    };

    //console.log(lstRepseInfo)
    var createCSVFile = new arrayToCsv(lstRepseInfo, {delimiter: ',', quote: '"'});

    await createCSVFile.saveFile('./ReporteRepse.csv')
                //.then(()=> console.log("Report Successfully Created"))
                //.catch(e => console.log("Error: Failed to create report"));
    var workerProcess = spawn('py', ['validacionSTPS_v2.py', '-p', csvPath]);  
        workerProcess.stdout.on('data', function (data) {  
            console.log('stdout: ' + data);   
            workerProcess.stderr.on('data', function (data) {  
                console.log('stderr: ' + data);  
            });  
            workerProcess.on('close', function (code) {  
                console.log('child process exited with code ' + code);  
            });  
        }); 
}

main()
