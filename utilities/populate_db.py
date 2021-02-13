import os
import pandas as pd
from OnlineBridge import db
from OnlineBridge.users.models import Role, Member

data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'OnlineBridge', 'static', 'data')
data_files = ['SpoXls.xls', 'guests.xlsx']

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
        for member_file in data_files:
            if member_file in os.listdir(data_dir):
                df = pd.DataFrame(pd.read_excel(
                    os.path.join(data_dir, member_file),
                    usecols=['NR', 'NAME', 'VNAME']
                ))

                df['NAME'] = [n.title() for n in df['NAME'].values]
                df['VNAME'] = [n.title() for n in df['VNAME'].values]

                for line in df.values:
                    if type(line[0]) == str:
                        db.session.add(Member(
                            guest_nr = line[0],
                            first_name = line[2],
                            last_name = line[1]
                        ))
                    else:
                        db.session.add(Member(
                            fed_nr = line[0],
                            first_name = line[2],
                            last_name = line[1]
                        ))
                db.session.commit()