from opcua import Client

url = "opc.tcp://212.205.81.18:4840/OPCUA/NORDEX-CIF-OPC-UA"

try:
    client = Client(url)

    client.connect()

    tm_voltage = client.get_node("ns=2;s=01CWE50208_analog_ANA000")
    print(tm_voltage.get_value())
    client.disconnect()
except Exception as err:
    print(err)
