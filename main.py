import re
import subprocess
import os
import sys
from datetime import date

CHM1_long = "/local/workdir/dmm2017/svnet/results/chm1-chm13/chm1.movie.bam"
CHM13_long = "/local/storage/data/chm1-13/CHM13/t2t/chm13_wm.bam"
CHM1_linked = "/local/storage/data/chm1-13/CHM1/CHM1_180GB_CrG_GRCh38_phased_possorted.bam"
CHM13_linked = "/local/storage/data/chm1-13/CHM13/CHM13_180GB_CrG_GRCh38_phased_possorted.bam"

all_datasets = [(CHM1_long, "chm1_long"), (CHM13_long, "chm13_long"), (CHM1_linked, "chm1_linked"), (CHM13_linked, "chm13_linked")]

def run():
    positions = []
    outdir = sys.argv[1]



    with open("positions.txt") as pos_file:
        for line in pos_file.readlines():
            current_pos = [x for x in re.split(':| |-|\n', line) if x]
            positions.append((current_pos[0], int(current_pos[1]), int(current_pos[2])))
    d = date.today().strftime("%b%d%Y")
    final_dir = os.path.join(outdir, "analysis_" + d)
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)

    bash_command_view_1 = "samtools view -hb "
    bash_command_index_1 = "samtools index "

    for position in positions:
        for filename, name in all_datasets:
            bash_command_view_2 = filename + " " + "\"" + position[0] + ":" + str(position[1] - 10000) + "-" + str(position[2] + 10000) + "\" " + \
                ">" + os.path.join(final_dir, position[0] + "-" + str(position[1]) + "-" + str(position[2])  + "_" + name + ".bam")
            full_view_command = bash_command_view_1 + bash_command_view_2
            print(full_view_command)
            subprocess.call(full_view_command.split())
            full_index_command = bash_command_index_1 + os.path.join(final_dir, position[0] + "-" + str(position[1]) + "-" + str(position[2])  + "_" + name + ".bam")
            subprocess.call(full_index_command.split())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
