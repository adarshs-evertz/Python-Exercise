import datetime
import uuid

import pytest

from models import Item


@pytest.fixture()
def jwts():
    yield {
        "AccessToken": "eyJraWQiOiI0WE15dEpYRVE0bWNiSkhXQjRQYW5uNW91VXptU2MyenVWNmRpRk5TNmd3PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIwYWQ0OGYxZS02OWVjLTRhZjgtOWUwZS03MTUxYjNmNDA2NjIiLCJldmVudF9pZCI6IjllM2M2MmFmLTljMGYtMTFlOC1iMDY0LTJiMDU2YTAxM2MzZCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE1MzM4NDUxNTIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5ldS13ZXN0LTEuYW1hem9uYXdzLmNvbVwvZXUtd2VzdC0xX3VjMHFsbWp0WCIsImV4cCI6MTUzMzg0ODc1MiwiaWF0IjoxNTMzODQ1MTUzLCJqdGkiOiI5ZDk2YTAyOS1mMmE2LTRjNjMtYjYyNy05NTY0OWQxYWUxMGIiLCJjbGllbnRfaWQiOiI1M3Zob3Y1cjBhdTZycjBqNzAzcmxtMDNsNSIsInVzZXJuYW1lIjoicm9vdCJ9.SdMk9ve6RIMN1TO1IVGMek0A1gZTLctrZrmCCJnE7Tba3DKXymGnfrOBNg1-eQgchUfvXwaVkgQZpE03-kwZpTe8hmhfVjd0AhIpRAE1_lv3tC_cnwsnIX-CmaWe6A1i1vLR91LjTg6joHqV8eUTHNNWCWKcoPpim2-B05e6yUk4fRX-hKTtHafpQRIdMpn2Wpp1PMkgq4vmyMzvU0-aZspzAlH0_CONjDWSa-pNvTaYwR41RZ_N09hlOPmY2fstAGymbA1LryjfX1lAZKi2Mq-RvHbZ_BAY8Eu96g8EnfaXsUd2FoxJRSDMIrN6zmENq40wMoYWi9shpFijd9g0Dg",
        "ExpiresIn": 3600,
        "TokenType": "Bearer",
        "RefreshToken": "eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBLU9BRVAifQ.CeNeLr5KGFIE_DXsExkrT5vkMmBEI7BdGShSq_-AJfpyoHIZH1ZYDDTS026Rw1h25lKA2CBolTiUEbo3fWc0TP3rx_HcQ2UojdkOOpGUMy7GLNktz7JOE1_ZwTivf7x07XkvZAwqQS_lL2SbPIYMYuDLjGEBGBwzxvhaK3FFz_fHBrwf7-UbysfzBu3YXLfiFb8bxkCoyIKm1o22fq-pIccF0quMSJmjk3SpfGZP5so4-7kuJN03rNTtf7EHFAfj_m9Q0KFfcMpuBBYCfjAkk2tsHrboF0u28hagssfBXfwk85v9jbDIK3AbLJCbHeDgueacSojwneSrQriKdBCQ4g.V2IaIZmqqePHeZVH.iXYiQohygmCeN0j3FESN-4gEfTXI_ZF8ybzruQbj9FMg29sQ9xAYWXAZwHqOOxvcqWklZhDa9oXaqYcRvfC7b7K6LOrUWfcLKrz1FQTUpwC8NHwB_iuzTEiG58IOFrDkAIvfJlG-NiscX0W7umsToxpy9hWrjy1AiLQePcOgjHVQWd0CNIkPtJiW9ue8wqR5MZU_zWcXnWdEpse3BXIEskwEbrgBP224ZMh3FXcrdPs33JOfkgAUSj8PK4GTCo4pvWpv7W4MI10tW4d8N024-MI8eYqVLD6dcgPy6fj9-kMKdveRa-mRP5JolVFqo7UpIzepaUtENFpIOEaX3_orK-vcbMCaI6rKqOhQ3VEVxPVGD71w9LsAbDFthc62Mkc05AAkbHLBfGrMWFTCLUXevFRyYU44rGM44gO39XA5cFBRtAEUn4gMd32jSuvgQntJnp-8w8nghx5NJ5saRmZ8wKAK2z7xhZ2GgY76RzMwMsuoeLi7-B2dSrYxBnCdojuyFiWBHIiaQ8v8tPT7pQX8WnKtIHJeCPvkAS-P9ASJpcfpffyrrglHVj1_GEUkiKuijSTSDTuv61h3h8CGa0Qv5U1F9eNPQK25mTbsTpPl19YIZl8FyyVdp6Wkx8NNi29p7qSjmDNmGex5laVGl9xp3UYZxajtOPDOS8LEw8I_w2nrGFzWEBpZfbs6Scns5Ubz60jl-eRBB4nLR-TBk7bzDWst7lypdtDH4OF_Wf-SBnVyw0GnoeeZdpIgF63SWKZ1GDBqJeo27Mmj0Xhk9Zq2lQ1n34bSzXSSHbCFXpTpHWw1Mo6jHyd2XWe2Ndd71tPCdcCKW6YDyTzxFpP4S19YSqOen9HHzEbrwzUAqQFN49lLTR7RJeSunVu2TpyG77ovgwOpxKmMr-CujFECgXDpZFn3p5guv5kkDe624a4s0q3WT5YHMuWW3Npnc3iO9w94xQGRUq6oC-9SRuzXGooJXBEaPeHBhnam2ZVURQYM0gJr0FiFFWCLorLR2tOm6I5ykYpatgwTmyko9mRebWBcazQ6bjBPPXpkZ61VIsmalZrqylEHX5I9ZC9QN_CHlSuKOC_TgDLabsu5PubZX4RM6EXfBPgd5JnrBLyuaoJrAHJRdY4vskKXOOZfwz0TyqIPsWFSGTP9QQdqCfiVaKXV7za6OXhZ9gTNo8CmLdLAU1BzgH5wRhpmxkRspUWJ0zVE4adB8OORfy2gPZCFNAIU9osD_N1Jlg5WuLA1ea07xNODSPpp3F59P-thF2v76nLgfw.aV3Eo9zw4iupANcFH9zl3A",
        "IdToken": "eyJraWQiOiJmQzVGdTM3VDh1R3hUVEhCRndiQzR6UVRmRHFLNTlKYXkyTlhzaXFwV0l3PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJmNGRiOTNjYy02OWQ2LTQyZjgtOWNlNy04OTU3NzZmMTc3ZjUiLCJhdWQiOiIzbmJpcmo0Y2JkMm5ja2tjaTA2cnA5Mzk5NCIsImV2ZW50X2lkIjoiY2YwNjBlMWEtY2M4NC0xMWU4LTk5OGYtMWI0ODIzZDMyZmFiIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE1MzkxNzMxNDEsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5ldS13ZXN0LTEuYW1hem9uYXdzLmNvbVwvZXUtd2VzdC0xX3h1V2xrc2J4diIsImNvZ25pdG86dXNlcm5hbWUiOiJyb290IiwiY3VzdG9tOnRlbmFudF9pZCI6IjAwMDAwMDAwLTAwMDAtMDAwMC0wMDAwLTAwMDAwMDAwMDAwMCIsImV4cCI6MTUzOTE3Njc0MSwiaWF0IjoxNTM5MTczMTQxLCJlbWFpbCI6ImdhbHRvbkBldmVydHouY29tIn0.PH0K2LZNdjmDOXfVwry9mV5sVf_ko3t3odJKoPuLu6BlvoIUnAj3YPFGoN_sRmo0iO0Lcu74q5Wd2NeoMexD3kWRKrHIBs9wjlFfg4vy2_HI0hscW1lkq2q7PcMzdjndX8nh-gNZia66AhFL8vwytV0a83NVtFOCcEf_3RFS-m7lkkuynQEOT5gugt4-WiUy1RjBknj-Xh5Bg-GOPsR1FBTU2JxejZ1la5tJk8O2JNYZNEyQAFM4DwDOHNyYRmUlEZYEZYNNu_ppFSp1DJnXeXy4061tTCW7jmCO5BUgTPSiZrPmnsV5NU-XUqC_3AllaQMKtP0soewN0llPHfQETw",
    }


# Sample APIGatewayEvent
@pytest.fixture()
def api_gateway_event():
    def _api_gateway_event(item_id: str, path: str, method: str, body: Item = None):
        request_id = str(uuid.uuid4())
        if body is None:
            body: Item = Item(text="test", success=True)

        request_context = {
            "httpMethod": method,
            "requestId": request_id,
            "path": path,
            "extendedRequestId": None,
            "resourceId": "123456",
            "apiId": "1234567890",
            "stage": "prod",
            "resourcePath": path,
            "identity": {
                "accountId": None,
                "apiKey": None,
                "userArn": None,
                "cognitoAuthenticationProvider": None,
                "cognitoIdentityPoolId": None,
                "userAgent": "Custom User Agent String",
                "caller": None,
                "cognitoAuthenticationType": None,
                "sourceIp": "127.0.0.1",
                "user": None,
            },
            "accountId": "123456789012",
            "domainName": "evertz.io",
            "domainPrefix": "",
            "routeKey": "test",
            "protocol": "HTTPS",
            "time": datetime.datetime.now().timestamp(),
            "timeEpoch": datetime.datetime.now(),
            "requestTime": datetime.datetime.now().timestamp(),
            "requestTimeEpoch": datetime.datetime.now(),
            "http": {
                "method": method,
                "path": path,
                "protocol": "HTTPS",
                "sourceIp": "127.0.0.1",
                "userAgent": "Mozilla",
            },
        }

        event = {
            "body": body.json(),
            "httpMethod": method,
            "resource": path,
            "queryStringParameters": {"foo": "bar"},
            "requestContext": request_context,
            "headers": {
                "Accept-Language": "en-US,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, sdch",
                "X-Forwarded-Port": "443",
                "CloudFront-Viewer-Country": "US",
                "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
                "CloudFront-Is-Tablet-Viewer": "false",
                "User-Agent": "Custom User Agent String",
                "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
                "CloudFront-Is-Desktop-Viewer": "true",
                "CloudFront-Is-SmartTV-Viewer": "false",
                "CloudFront-Is-Mobile-Viewer": "false",
                "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Upgrade-Insecure-Requests": "1",
                "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
                "X-Forwarded-Proto": "https",
                "Cache-Control": "max-age=0",
                "CloudFront-Forwarded-Proto": "https",
            },
            "multiValueHeaders": {},
            "stageVariables": None,
            "path": path,
            "pathParameters": {
                "id": request_id,
                "item_id": item_id,
            },
            "isBase64Encoded": False,
            "version": 1.1,
            "rawPath": path,
            "rawQueryString": "test",
            "routeKey": "test",
        }

        class Context(object):
            aws_request_id = event["requestContext"]["requestId"]

        return event, Context()

    return _api_gateway_event


@pytest.fixture()
def get_correct_item_event(jwts, api_gateway_event):
    event, context = api_gateway_event("1", "/get_item/1", "GET")
    event["headers"]["Authorization"] = jwts["IdToken"]
    yield event, context


@pytest.fixture()
def get_item_without_jwt_event(jwts, api_gateway_event):
    event, context = api_gateway_event("1", "/get_item/1", "GET")
    yield event, context


@pytest.fixture()
def get_not_existing_item_event(jwts, api_gateway_event):
    event, context = api_gateway_event("999", "/get_item/999", "GET")
    event["headers"]["Authorization"] = jwts["IdToken"]
    yield event, context

@pytest.fixture()
def update_correct_item_event(jwts, api_gateway_event):
    event, context = api_gateway_event("1", "/update_item/1", "PATCH")
    event["headers"]["Authorization"] = jwts["IdToken"]
    yield event, context


@pytest.fixture()
def update_item_without_jwt_event(jwts, api_gateway_event):
    event, context = api_gateway_event("1", "/update_item/1", "PATCH")
    yield event, context


@pytest.fixture()
def update_not_existing_item_event(jwts, api_gateway_event):
    event, context = api_gateway_event("999", "/update_item/999", "PATCH")
    event["headers"]["Authorization"] = jwts["IdToken"]
    yield event, context
