import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout
from robot.api.deco import keyword
import logging
import time
import ast
import json

class XAPI:
    @keyword("XGet Response API")
    def get_response_api(self, url, headers=None, method="GET", payload=None, retries=3, timeout=10, verify_ssl=True, allow_redirects=True, json_response=True):
        """
        ***|    Description     |***
        |   *`Get API Token`*   |   คืนค่า JSON จากการยิง API เพื่อรับ token และสามารถทำงานกับ API ทั่วไปได้ |

        ***|    Example     |***
        | *`${response}`* | *`Get API Token`* | *`https://example.com/api/token`* | *`${headers}`* | *`GET`* | *`${payload}`* | *`3`* | *`10`* | *`${true}`* | *`${true}`* | *`${true}`* |
        | *`Log`* | *`Response: ${response}`* |

        ***|    Parameters     |***
        - `url`: API URL
        - `headers`: Dictionary ของ headers ที่จะใช้ใน request (ค่าเริ่มต้นคือ None)
        - `method`: HTTP method ที่จะใช้ (ค่าเริ่มต้นคือ GET)
        - `payload`: ข้อมูลที่จะส่งไปกับ request (ค่าเริ่มต้นคือ None)
        - `retries`: จำนวนครั้งที่พยายามหากเกิดข้อผิดพลาด (ค่าเริ่มต้นคือ 3)
        - `timeout`: เวลาที่ให้ request ทำงานก่อนหมดเวลาในหน่วยวินาที (ค่าเริ่มต้นคือ 10)
        - `verify_ssl`: ตรวจสอบ SSL certificate หรือไม่ (ค่าเริ่มต้นคือ True)
        - `allow_redirects`: อนุญาตให้ redirect หรือไม่ (ค่าเริ่มต้นคือ True)
        - `json_response`: แปลงผลลัพธ์เป็น JSON หรือไม่ (ค่าเริ่มต้นคือ True)

        *`Create By Tassana Khrueawan`*
        """
        if isinstance(headers, str):
            headers = ast.literal_eval(headers)

        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except json.JSONDecodeError:
                logging.warning("Payload is not a valid JSON string. Using it as-is.")

        attempt = 0
        while attempt < retries:
            try:
                if method.upper() == "GET":
                    response = requests.get(url, headers=headers, params=payload, timeout=timeout, verify=verify_ssl, allow_redirects=allow_redirects)
                elif method.upper() == "POST":
                    response = requests.post(url, headers=headers, json=payload, timeout=timeout, verify=verify_ssl, allow_redirects=allow_redirects)
                elif method.upper() == "PUT":
                    response = requests.put(url, headers=headers, json=payload, timeout=timeout, verify=verify_ssl, allow_redirects=allow_redirects)
                elif method.upper() == "DELETE":
                    response = requests.delete(url, headers=headers, json=payload, timeout=timeout, verify=verify_ssl, allow_redirects=allow_redirects)
                elif method.upper() == "PATCH":
                    response = requests.patch(url, headers=headers, json=payload, timeout=timeout, verify=verify_ssl, allow_redirects=allow_redirects)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                response.raise_for_status()

                if json_response:
                    try:
                        return response.json()
                    except json.JSONDecodeError:
                        logging.warning("Response is not JSON. Returning text content.")
                        return response.text
                else:
                    return response.text

            except (HTTPError, ConnectionError, Timeout) as err:
                logging.error(f"Request failed: {err}")
                attempt += 1
                if attempt < retries:
                    logging.info(f"Retrying... Attempt {attempt}/{retries}")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logging.error("Max retries exceeded")
                    raise HTTPError(f"Max retries exceeded: {err}")

            except Exception as err:
                logging.error(f"An unexpected error occurred: {err}")
                raise

        return None  # This line will only be reached if all retries fail