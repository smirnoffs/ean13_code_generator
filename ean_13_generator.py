import csv

import click


@click.command()
@click.option('--diapason_start', type=int, help='The start of the diapason')
@click.option('--diapason_end', type=int, help='The end of the diapason')
@click.option('--amount', type=int, default=1)
@click.option('--output_file', type=str, default='ean_codes.csv')
def generate(diapason_start, diapason_end, amount, output_file):
    """
    The command for generating EAN-13 barcode numbers with checksum digit
    """
    if not diapason_start:
        raise click.ClickException('diapason_start is required')
    if diapason_end and amount:
        raise click.ClickException('Provide the amount of codes or the end of the diapason, not both')
    if diapason_end is None:
        diapason_end = int(diapason_start) + int(amount)
    with open(output_file, 'w') as output_file:
        writer = csv.writer(output_file)
        for code_number in range(diapason_start, diapason_end + 1):
            chcksum = calculate_checksum(code_number)
            full_code = '{}{}'.format(code_number, chcksum)
            writer.writerow([full_code, ])
            print(full_code)


def calculate_checksum(code_number):
    weight = [1, 3] * 6
    magic = 10
    chck_sum = 0

    for i in range(12):
        chck_sum = chck_sum + int(str(code_number)[i]) * weight[i]
    z = (magic - (chck_sum % magic)) % magic
    if z < 0 or z >= magic:
        return None
    return z


if __name__ == '__main__':
    generate()
