sudo modprobe cp210x
echo 10c4 0001 | sudo tee /sys/bus/usb-serial/drivers/cp210x/new_id
echo 10c4 0005 | sudo tee /sys/bus/usb-serial/drivers/cp210x/new_id
sudo chmod 666 /dev/ttyUSB0
sudo chmod 666 /dev/ttyUSB1
