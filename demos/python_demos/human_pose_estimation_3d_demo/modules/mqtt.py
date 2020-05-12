import numpy as np
import time
from scipy.spatial.distance import pdist, squareform

MINDISTANCE = 150


def on_publish(client, userdata, result):  # create function for callback
    print(">> mqtt - Message (" + str(result) + ") succeed to be published ")
    pass


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(">> mqtt - connected with server")


def send_poses(client, topic, frame, poses_3d):
    """

    :param client: MQTT Client
    :param topic: String, Topic to sent
    :param frame: Frame number
    :param poses_3d: Poses_3d, a collection of 19 points (x, y, z)
    :return: dict, poses_3d that have a distance less that MINDISTANCE
    """

    localtime = time.strftime("%d/%m/%Y-%H:%M:%S", time.localtime())

    necks = []
    for id, pose in enumerate(poses_3d, 0):
        necks.append(pose[1])
        load = ''
        for point in pose:
            load = load + str(point[0]) + ',' + str(point[1]) + ',' + str(point[2]) + ' '
        total = localtime + ' ' + str(frame) + ' ' + str(id) + ' ' + load
        client.publish(topic, total)

    distances = squareform(pdist(necks))

    poses = dict()
    for i, distance in enumerate(distances, 0):
        min = np.where(np.logical_and(distance > 0., distance <= MINDISTANCE))
        min = min[0].tolist()
        if min:
            poses[i] = min[0]

    return poses
