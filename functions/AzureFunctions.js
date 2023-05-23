const fs = require('fs');
const AdmZip = require("adm-zip");

const extractRarArchive = require("./rarfiles");
const downloadFile = require('../azure/Azure');

const comprobarRuta = (path)=>{
    if(!fs.existsSync(path))
    try{
        fs.mkdirSync(path);
        console.log(`${path} creada con éxito`);
    } catch(err) {
        throw err;
    }
}

const crearRutas = (rootPath, dataFile)=>{
    comprobarRuta(rootPath);// el Datafile y el path no deberían pasarse como parametro?
    dataFile.map( item =>{
        const nameDirectory =  item.RazonSocial.replace(/\s+/,' ');
        const path = `${ rootPath }/${ nameDirectory }`;
        comprobarRuta(path);
    });
}

const descargarBlobs = async (dataFile, path) =>{
    await Promise.all(
        dataFile.map( async item =>{
            let pathDownload = `./${ path }/`//`./${ path }/${ item.RazonSocial.replace(/\s+/,' ') }`;
            await downloadFile(item.Path,`${ pathDownload }`);
        })
    )
    //descomprimirArchivo(path);
    console.log("Descarga finalizada")
}

const descomprimirArchivo = (path) => {
    const carpetas = fs.readdirSync(path); 

    carpetas.map( carpeta => {
        const archivos = fs.readdirSync(path+"/"+carpeta);
        archivos.map( archivo => {

            const archivePath = path+"/"+carpeta+"/"+archivo;
            try {
                fs.mkdirSync(archivePath.replace(".zip","")
                                        .replace(".rar",""));

                if(archivo.includes(".zip")) 
                    AdmZip(archivePath).extractAllTo(archivePath.replace(".zip",""));
                if(archivo.includes(".rar"))
                    extractRarArchive(archivePath, archivePath.replace(".rar",""));
                console.log(">>>> "+archivo+" extraido correctamente")
            } catch(err) {
                console.log(err);
            }
        });
    });
    
}

module.exports = {crearRutas, descargarBlobs};
