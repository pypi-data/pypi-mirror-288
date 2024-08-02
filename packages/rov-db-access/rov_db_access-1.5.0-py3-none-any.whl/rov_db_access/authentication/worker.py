from datetime import datetime
from sqlalchemy import select

from rov_db_access.config.db_utils import init_db_engine
from rov_db_access.config.settings import Settings
from rov_db_access.logging.utils import logger
from sqlalchemy.orm import Session
from rov_db_access.authentication.models import AssociationUserRole, Organization, Role, UnverifiedUser, User

settings = Settings()


class UserExistsException(Exception):
    pass


class UserNotExistsException(Exception):
    pass


class AuthenticationWorker:

    def __init__(self) -> None:

        self.engine = init_db_engine(
            settings.db_rov_proxy_user,
            settings.db_rov_proxy_password,
            settings.db_rov_proxy_host,
            settings.db_rov_proxy_port,
            settings.db_rov_gis_database
        )

    def get_user_by_username(self, username: str):
        with Session(self.engine) as session:
            user_query = (
                select(User)
                .where(User.username == username)
                .limit(1)
            )
            user = session.scalar(user_query)
            if user is None:
                logger.warning(f'Cannot get user. username={username} does not exists.')
                raise UserNotExistsException(f'User Username: {username} does not exists')
            roles = user.roles
            return {"user": user, "user_roles": roles}

    def get_user_by_email(self, email: str):
        with Session(self.engine) as session:
            user_query = (
                select(User)
                .where(User.email == email)
                .limit(1)
            )
            user = session.scalar(user_query)
            if user is None:
                logger.warning(f'Cannot get user. email={email} does not exists.')
                raise UserNotExistsException(f'User Email: {email} does not exists')
            roles = user.roles
            return {"user": user, "user_roles": roles}

    def get_user_by_id(self, user_id: int):
        with Session(self.engine) as session:
            user = session.get(User, user_id)
            if user is None:
                logger.warning(f'Cannot get user. id={user_id} does not exists.')
                raise UserNotExistsException(f'User Id: {user_id} does not exists')
            roles = user.roles
            return {"user": user, "user_roles": roles}

    def create_user(self, username: str, password: str, email: str):
        with Session(self.engine) as session:
            # Check if user with username already exists
            user_query = (
                select(User)
                .where(User.username == username)
                .limit(1)
            )
            user = session.scalar(user_query)
            if user is not None:
                logger.warning(f'Cannot create user because verified username already exists. username={username}')
                raise UserExistsException(f'User Username: {username} already exists')
            # check if user with email already exists
            user_query = (
                select(User)
                .where(User.email == email)
                .limit(1)
            )
            user = session.scalar(user_query)
            if user is not None:
                logger.warning(f'Cannot create user because verified email already exists. email={email}')
                raise UserExistsException(f'User email: {email} already exists')
            new_user = User(username=username, password=password, email=email)
            session.add(new_user)
            session.commit()
            new_user_id = new_user.id
            return new_user_id

    def create_unverified_user(self, username: str, display_name: str, password: str, email: str, expires_at: datetime):
        with Session(self.engine) as session:
            # Check if user with username already exists
            user_query = (
                select(User)
                .where(User.username == username)
                .limit(1)
            )
            user = session.scalar(user_query)
            if user is not None:
                logger.warning(f'Cannot create unverified user because verified username already exists. username={username}')
                raise UserExistsException(f'User Username: {username} already exists')
            # check if user with email already exists
            user_query = (
                select(User)
                .where(User.email == email)
                .limit(1)
            )
            user = session.scalar(user_query)
            if user is not None:
                logger.warning(f'Cannot create unverified user because verified email already exists. email={email}')
                raise UserExistsException(f'User email: {email} already exists')
            user_query = (
                select(UnverifiedUser)
                .where(UnverifiedUser.username == username)
                .limit(1)
            )
            user = session.scalar(user_query)
            if user is not None:
                logger.warning(f'Cannot create unverified user because unverified username already exists. username={username}')
                raise UserExistsException(f'User Username: {username} already exists')
            user_query = (
                select(UnverifiedUser)
                .where(UnverifiedUser.email == email)
                .limit(1)
            )
            user = session.scalar(user_query)
            if user is not None:
                logger.warning(f'Cannot create unverified user because unverified email already exists. email={email}')
                raise UserExistsException(f'User email: {email} already exists')

            new_unverified_user = UnverifiedUser(username=username, display_name=display_name, password=password, email=email, expires_at=expires_at)
            session.add(new_unverified_user)
            session.commit()
            new_unverified_user_id = new_unverified_user.id
            return new_unverified_user_id

    def load_user(self, id: str):
        with Session(self.engine) as session:
            user = session.get(User, id)
            if user is None:
                logger.warning(f'Cannot get user. id={id} does not exists.')
                raise UserNotExistsException(f'User Id: {id} does not exists')
            return {
                "id": user.id,
                "username": user.username,
                "logged_at": user.logged_at,
                "organization_id": user.organization_id
            }

    def load_users_by_org(self, organization_id: str):
        with Session(self.engine) as session:
            query_users = (
                select(User)
                .where(User.organization_id == organization_id)
                .order_by(User.id)
            )
            users = session.scalars(query_users).all()
            if users is None or len(users) == 0:
                logger.warning(f'No users found! for this org_id={organization_id}')
                return []
            else:
                results = []
                for user in users:
                    results.append({
                        "id": user.id,
                        "username": user.username,
                        "logged_at": user.logged_at,
                        "organization_id": user.organization_id
                    })
                return results

    def user_verification(self, unverified_user_id: int):
        with Session(self.engine) as session:
            unverified_user = session.get(UnverifiedUser, unverified_user_id)
            if unverified_user is None:
                logger.warning(f'No unverified user with id={unverified_user_id} found')
                raise Exception(f'No unverified user with id {unverified_user_id} found!')
            user_org = Organization(name=unverified_user.username+"_org")
            session.add(user_org)
            session.commit()
            new_user = User(
                username=unverified_user.username,
                display_name=unverified_user.display_name,
                password=unverified_user.password,
                email=unverified_user.email,
                organization_id=user_org.id
            )
            session.add(new_user)
            session.delete(unverified_user)
            session.commit()
            inference_role_query = (
                select(Role)
                .where(Role.name == "inference")
                .limit(1)
            )
            inference_role = session.scalar(inference_role_query)
            association_user_role = AssociationUserRole(user_id=new_user.id, role_id=inference_role.id)
            session.add(association_user_role)
            session.commit()
            new_user_display_name = new_user.display_name
            return new_user_display_name

    def update_user_last_login(self, user_id: int):
        with Session(self.engine) as session:
            user = session.get(User, user_id)
            if user is None:
                logger.warning(f'Cannot update user. id={user_id} does not exists.')
                raise UserNotExistsException(f'User Id: {user_id} does not exists')
            user.logged_at = datetime.now()
            session.commit()

    def get_org_by_id(self, org_id: int):
        with Session(self.engine) as session:
            organization = session.get(Organization, org_id)
            if organization is None:
                logger.warning(f'Cannot get Organization. id={org_id} does not exists.')
                raise UserNotExistsException(f'Organization Id: {org_id} does not exists')
            return organization

    def use_credits(self, org_id, credits_to_use: float):
        with Session(self.engine) as session:
            organization = session.get(Organization, org_id)
            if organization is None:
                logger.warning(f'Cannot update Organization. id={org_id} does not exists.')
                raise UserNotExistsException(f'Organization Id: {org_id} does not exists')
            organization.credits -= credits_to_use
            session.commit()
            return organization.credits
