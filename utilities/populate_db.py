import os
import pandas as pd
from OnlineBridge import db, app, MEMBER_FILENAME, MEMBER_MAPPING
from OnlineBridge.users.models import Role, Member, User

data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'OnlineBridge', 'static', 'data')
data_files = [MEMBER_FILENAME, 'guests.xlsx']

def populate():
    # roles
    required_roles = ['Superuser', 'Admin', 'Director', 'Player']

    for role in required_roles:
        if Role.query.filter_by(name=role).first() is None:
            nr = Role(name=role)
            db.session.add(nr)
            db.session.commit()

    #members
    if Member.query.count() == 0:
        for index, member_file in enumerate(data_files):
            # build add member command
            inner_part = ','.join(
                [f'{k}=df.loc[line,"{v}"]' for k,v in MEMBER_MAPPING.items()]
            )
            command = f'Member({inner_part})'
            if index == 1:
                # guests
                command = command.replace('fed_nr', 'guest_nr')
            # else:
            #     continue

            if member_file in os.listdir(data_dir):

                df = pd.DataFrame(pd.read_excel(
                    os.path.join(data_dir, member_file),
                    usecols=MEMBER_MAPPING.values()
                ))

                for line in range(len(df)):
                    member = eval(command)
                    member.first_name = member.first_name.title()
                    member.last_name  = member.last_name.title()

                    # converting from np.int64
                    if member.fed_nr:
                        member.fed_nr = int(member.fed_nr)

                    db.session.add(member)

                    db.session.commit()

    # assign superuser
    user = User.query.filter_by(email=app.config['MAIL_USERNAME']).first()
    if user:
        user.roles = Role.query.all()
        db.session.add(user)
        db.session.commit()