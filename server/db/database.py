import asyncpg
class Database:
    def __init__(self,user,password,host,database,logger,port="5432"):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self._cursor = None
        self.logger = logger
        self._connection_pool = None
        
    async def connect(self):
        if not self._connection_pool:
            try:
                self._connection_pool = await asyncpg.create_pool(
                    min_size=1,
                    max_size=20,
                    command_timeout=60,
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
                self.logger.info("Database pool connectionn opened")

            except Exception as e:
                self.logger.exception(e)

    async def fetch_rows(self, query: str,*args):
        if not self._connection_pool:
            await self.connect()
        else:
            con = await self._connection_pool.acquire()
            try:
                result = await con.fetch(query,*args)
                return result
            except Exception as e:
                self.logger.exception(e)
            finally:
                await self._connection_pool.release(con)


    async def save_row(self, query: str, *args):
        if not self._connection_pool:
            await self.connect()
        else:
            con = await self._connection_pool.acquire()
            try:
                result = await con.execute(query,*args)
                return result
            except Exception as e:
                self.logger.exception(e)
            finally:
                await self._connection_pool.release(con) 

    async def close(self):
        if not self._connection_pool:
            try:
                await self._connection_pool.close()
                self.logger.info("Database pool connection closed")
            except Exception as e:
                self.logger.exception(e)