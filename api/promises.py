import asyncio



#astart() starts unawaited async tasks declared at this level
async def astart():
  a=await asyncio.sleep(0)
  return a
async def promise(task,parameters):
  task = asyncio.create_task(task(*parameters))
  await astart();
  return task
def none():
  return None
def Q(function,parameters):
  try:
    return function(*parameters)
  except:
    return None
async def AQ(function,parameters):
  try:
    return await function(*parameters)
  except:
    return None
false = False
true = True