const fs = require('fs');
const { type } = require('os');

class arrayToCsv {

    constructor(data = [], params = {
        delimiter: ',',
        quote: '"'
    }){
        this.delimiter = params.delimiter;
        this.quote = params.quote;
        this.data = data;
        this.csv = '';

        var aHeaders = [];

        //Generate the csv data
        this.data.forEach((row, index) => {

            if(index === 0){
                //Headers from first element
                Object.keys(row).forEach((elem, index, array) => {

                    if(index === array.length-1){
                        this.csv += this.quote + elem + this.quote + '\n';
                    }else{
                        this.csv += this.quote + elem + this.quote + this.delimiter;
                    }

                    aHeaders.push(elem);
                });

                //data
                aHeaders.forEach((elem, index, array) => {

                    //Last element
                    if(index === array.length-1){

                        this.csv += this.quote + row[elem] + this.quote + '\n';
                        
                    }else{

                        this.csv += this.quote + row[elem] + this.quote + this.delimiter;
                        
                    }
                });

            }else{
                //data
                aHeaders.forEach((elem, index, array) => {

                    //Last element
                    if(index === array.length-1){

                        this.csv += this.quote + row[elem] + this.quote + '\n';

                    }else{

                        this.csv += this.quote + row[elem] + this.quote + this.delimiter;
                        
                    }
                });
            }

        });

    }

    getCsv(){
        return this.csv;
    }

    saveFile(path){
        return new Promise((resolve, reject) => {

            if(this.csv){
                fs.writeFileSync(path, this.csv, {encoding: 'latin1'});
                resolve('OK');
            }else{
                reject('Error, no csv data generate');
            }

        });
    }
}

module.exports = arrayToCsv;