let extrac = require('node-unrar-js');


async function extractRarArchive(file, destination) {
  try {
    const extractor = await extrac.createExtractorFromFile({
      filepath: file,
      targetPath: destination
    });

    [...extractor.extract().files];
  } catch (err) {
    console.error(err);
  }
}

module.exports = extractRarArchive;