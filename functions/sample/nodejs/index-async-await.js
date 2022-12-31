const { CloudantV1 } = require("@ibm-cloud/cloudant");
const { IamAuthenticator } = require("ibm-cloud-sdk-core");

async function main(params) {
  const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
  const cloudant = CloudantV1.newInstance({
    authenticator: authenticator,
  });
  cloudant.setServiceUrl(params.COUCH_URL);
  let response = null;
  try {
    if (params.state) {
      const selector = {
        state: {
          $eq: params.state,
        },
      };
      response = await cloudant.postFind({
        db: "dealerships",
        selector: selector,
      });
      return { response: response.result.docs };
    } else if (params.dealerId) {
      const selector = {
        id: {
          $eq: parseInt(params.idealerId),
        },
      };
      response = await cloudant.postFind({
        db: "dealerships",
        selector: selector,
      });
      return { response: response.result.docs };
    } else {
      response = await cloudant.postAllDocs({
        db: "dealerships",
        includeDocs: true,
      });
    }
    return response.result;
  } catch (error) {
    return { error: error.description };
  }
}
