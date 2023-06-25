## Replace Below ENV Vars

export GITHUB_TOKEN=<GITHUB API TOKEN>
#Please follow this link to generate token https://github.com/settings/tokens
export GITHUB_USERNAME=#<github repo username>
export GITHUB_REPO=#<github repo name>


export SENDER_EMAIL=#<provide sender gmail adress>
export RECEIVER_EMAIL=#<receiver gmail address>
export SMTP_SERVER=#"smtp.gmail.com" <replace gmail server here>
export SMTP_PORT=587 #<Replace gmail port>
export SMTP_USERNAME=#<provide gmail sender address >
export SMTP_PASSWORD=#<generated app gmail api token>
    #Please follow api token generation here https://support.google.com/accounts/answer/185833?visit_id=638232731515859823-2397466037&p=InvalidSecondFactor&rd=1

python3.10 script.py
