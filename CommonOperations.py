import json

import DevicePushObject
from gcm import GCM


def getDeviceByID(deviceId):
    device = DevicePushObject.Devices.query(DevicePushObject.Devices.deviceId == str(deviceId)).fetch()
    return device if len(device) != 0 else None


def cacheDevice(deviceId, pushKey):
    devices = getDeviceByID(deviceId)
    if devices is not None:
        for device in devices:
            device.pushKey = pushKey
            device.put()
    else:
        newDevice = DevicePushObject.Devices(
                deviceId=deviceId,
                pushKey=pushKey
        )
        newDevice.put()


def getReceiver(emailAddress):
    index = str(emailAddress).find('@')
    return emailAddress[:index]


def sendPushToRecipient(data, senderEmail, recipient):
    gcm = GCM('gcm_key')
    data = {'message': data, 'sender': senderEmail, 'type': 200}
    gcm.json_request(registration_ids=recipient, data=data)
