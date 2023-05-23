const XLSX = require('xlsx');
let dataExcel = []

const leerExcel = (documento) => {
    const workbook = XLSX.readFile(documento);
    const workbookSheets = workbook.SheetNames;
    dataExcel = XLSX.utils.sheet_to_json(workbook.Sheets[workbookSheets[0]]);
    return dataExcel
}

const convertirBase64 = async (documento)=>{
    return new Promise( (resolve) =>{
        const doc = `./docs/pdfs/${documento}`;
        let binaryData = fs.readFileSync(doc);
        resolve(new Buffer(binaryData).toString('base64'));
    })
}

module.exports = {leerExcel, convertirBase64}