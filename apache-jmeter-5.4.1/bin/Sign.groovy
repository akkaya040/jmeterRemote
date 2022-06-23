import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.security.InvalidKeyException;
import groovy.json.JsonSlurper;

def hmac_sha256(String secretKey, String data) {
try {
Mac mac = Mac.getInstance(“HmacSHA256”)
SecretKeySpec secretKeySpec = new SecretKeySpec(secretKey.getBytes(), “HmacSHA256”)
mac.init(secretKeySpec)
byte[] digest = mac.doFinal(data.getBytes())
return digest
} catch (InvalidKeyException e) {
throw new RuntimeException(“Invalid key exception while converting to HMac SHA256”,e)
}
}

def generatePayLoad(String apiKey,String fileName)
{

try{
def payload = new File(fileName).getText()
/* Commenting below as this is an overhead and is not needed */
/* def jsonSlurper = new JsonSlurper()
def parsedJSONPayload = jsonSlurper.parseText(payload).toString()
*/
String b64encodedPayload = payload.bytes.encodeBase64().toString()
def hash = hmac_sha256(apiKey,b64encodedPayload)
def encodedHash = hash.encodeBase64().toString()
return (encodedHash + ‘.’ + b64encodedPayload)

}catch(ex){
throw new RuntimeException(“Exception Caught while Creating payload”,ex)
}

}
/* Entry Point to the Script */
/* Parameters are passed from the JSR223 Sampler in Jmeter*/
def apiKey = args[0]
def fileName = args[1]

def payloadRt = generatePayLoad(apiKey,fileName)
return(payloadRt)