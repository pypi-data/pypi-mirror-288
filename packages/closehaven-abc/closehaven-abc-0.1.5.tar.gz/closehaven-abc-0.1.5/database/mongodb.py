import certifi
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from base_utils.exception import ImproperConfigurationError
import asyncio
from config import host,username,password,prod,db_name


client: AsyncIOMotorClient | None = None

async def init(test: bool, loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()) -> None:
	global client
	global db_name
	conn_params = {
		'host': host,
		'username': username,
		'password': password,
	}
	
	if all(conn_params.values()):
    #ABCDEF must expose it to all models or routes by settings file
		client = AsyncIOMotorClient(
    	host=f"mongodb+srv://{conn_params['host']}/?retryWrites=true&w=majority",
			username=conn_params['username'],
			password=conn_params['password'],
			uuidRepresentation='standard',
			tlsCAFile=certifi.where(),
			io_loop=loop,
		)
  
		print(await client.server_info())
	else:
		raise ImproperConfigurationError('Problem with MongoDB environment variables')

	if prod == 'false' and not test:
		db_name += '_dev'
	elif prod == 'false' and test:
		db_name += '_test'
  
	if db_name is not None:
		await init_beanie(database=client[db_name], document_models=[
			"application.models.Application",
			"user.models.User",
			"user_notification.models.UserNotification",
			"role.models.Role",
			"organization.models.Organization",
			"member.models.Member",
    ],
    allow_index_dropping = True,
    recreate_views=True
    )

		return client, db_name
	else:
		raise ImproperConfigurationError('Problem with MongoDB environment variables')
