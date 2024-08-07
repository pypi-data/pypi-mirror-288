from django.core.mail import send_mail, BadHeaderError
import random,db,time
import logging

logger = logging.getLogger(__name__)

def login_otp(token_type, token,request):
    from django.contrib.auth import authenticate
    from django.contrib.auth import login as auth_login
    from . import google_login
    user = authenticate(token_type, token=token)
    if user is not None:
        auth_login(request, user)
    try:
        db.create('SignupActivity',{'user':user})
        # google_login.create_user_entry_log(user.id, request.COOKIES['_ga'])
    except:
        pass
    return {'success':True}

def generate_otp():
    otp = str(random.randint(1000,9999))
    return otp

def send_email(email,request):
    Otp = generate_otp() 
    body_html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
        </head>
        <body>
            <div style="width: 100%; height: 100%;">
        
            <div class="header" style="width: 100%;">
                <a href="http://easyinsights.ai" target="_blank"><img style="height:88px; width:700px;"
                    src="https://app.easyinsights.ai/static/emailBanner.png" alt="EasyInsights"></a>
            </div>
            
            <div style="margin-left: 12%;">
                <p style="height: 30px;  font-family: Arial; text-align: left;
                font-size: 22px; font-weight: 700; line-height: 30px; letter-spacing: 0.03em;">Confirm your email address</p>
                
            
                <div class="letter-content" style="width: 500px; height: 45px; flex-shrink: 0; font-family: Arial; font-size: 15px; font-weight: 400;
                line-height: 23px; letter-spacing: 0.03em; text-align: left; margin-bottom:15px;">
                    Your confirmation code is below — enter it in your open browser window to sign in to EasyInsights.
                    
                </div>

            
                <div style="width: 454px; height: 70px; display: table-cell;text-align: center; vertical-align: middle;
                background-color:#F6F5FA; margin: 10px 0px;">
                    <span style="font-family: Arial; font-size: 28px; font-weight: 400; line-height: 42px;
                    letter-spacing: 0.03em;">{Otp}</span>
                </div>
                
                <div class="letter-content" style="width: 500px; height: 45px; flex-shrink: 0; font-family: Arial; font-size: 15px; font-weight: 400;
                line-height: 23px; letter-spacing: 0.03em; text-align: left; margin-top:24px; margin-bottom:90px">
                Feel free to reach out to us if you have any questions, feedback, or suggestions. We'd love to hear from you!
                </div>

                

                <div class="ft-div" style="display: table-cell; width: 700px; height:203px; flex-direction: column; margin: 15px;">
                    <div style="width:454px; vertical-align: middle; text-align:center;margin-bottom: 15px; margin-top: 15px;">
                       <img style="height:27px; width:127px;"
                           src="https://app.easyinsights.ai/static/Logo.png" alt="EasyInsights">
                   </div>
                   <div class="m-bottom" style="display: table-cell; width: 454px; vertical-align: middle; text-align: center;">
                       <a href="https://www.facebook.com/profile.php?id=100063985839525" target="_blank"><img class="icn" style="height: 30px; width: 30px;" src="https://easyinsights.ai/assets/images/emailResponse/facebook-icon.png" alt="facebook"></a>
                       <a href="https://twitter.com/easy_insights" target="_blank"><img class="icn" style="height: 30px; width: 30px;" src="https://easyinsights.ai/assets/images/emailResponse/twitter-icon.png" alt="twitter"></a>
                       <a href="https://in.pinterest.com/EasyInsights_121/" target="_blank"><img class="icn" style="height: 30px; width: 30px;" src="https://easyinsights.ai/assets/images/emailResponse/pinterest-icon.png" alt="pinterest"></a>
                       <a href="https://www.linkedin.com/company/easyinsights/" target="_blank"><img class="icn" style="height: 30px; width: 30px;" src="https://easyinsights.ai/assets/images/emailResponse/linkedin-icon.png" alt="linkedin"></a>
                       <a href="https://www.instagram.com/easyinsights.ai/" target="_blank"><img class="icn" style="height: 30px; width: 30px;" src="https://easyinsights.ai/assets/images/emailResponse/instagram-icon.png" alt="instagram"></a>
                   </div>
       
                   <div class="footer" style="color:#000; font-family:Arial;font-size:14px;font-style:normal;font-weight:400;
                           line-height:120.5%; letter-spacing:0.42px">
                       <p>EasyInsights, 14-04 160 Robinson Rd, Singapore, Singapore, 068914</p>
                   </div>
       
               </div>
            </div> 

        </div>
    
        </body>
        </html>
        '''
    try:
        send_mail( subject="Email OTP to Sign in", message=f'your OTP is : {Otp}',html_message=body_html,from_email= "hello@easyinsights.com",recipient_list= [email],fail_silently=False)
        request.session['otp'] = {"value":Otp,"ts": int(time.time()),"email":email}
        return {'success':True,'message':"otp sent"}
    except BadHeaderError:
            return {'success':False,'message':"Invalid header found."}
    except Exception as e:
        logger.error(e, exc_info=True)
        return {'success':False,'message':"error occured"}


def verify(data,request):
    try:
        if (request.session['otp']['value'] == data['otp'] and (int(time.time())-request.session['otp']['ts'] <= 300)):
            token = request.session['otp']['email']
            user = login_otp('otp', token,request)
            return {'success':True,'message':'otp verified'}
        else:
            return {'success':False,'message':'wrong otp or Invalid otp'}
    except Exception as e:
        logger.error(e, exc_info=True)
        return {'sucess':False,'message':"please try again"}

