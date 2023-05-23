const { BlobServiceClient } = require('@azure/storage-blob');

// const storageName = 'glwinbastorage';
const connString = process.env.AZURE_STORAGE_ACCOUNT_NAME;

if(!connString) throw Error('Azure Conecction String not found');

//cliente
const client = BlobServiceClient.fromConnectionString(connString);
const containerServicios = client.getContainerClient('servicios-especializados');
let descarga = 0;

async function downloadBlobToFile(containerClient, blobName, fileNameWithPath) {
    try{
        const blobClient = await containerClient.getBlobClient(blobName);
        await blobClient.downloadToFile(fileNameWithPath);
        console.log(`download of ${blobName} success ${descarga++}`);
    }catch(err){
        console.log('Error al descargar el blob',err.message);
    }
}

module.exports = { containerServicios, downloadBlobToFile };