from easy_kubeflow import EasyJobs, JobSpec

if __name__ == '__main__':
    runs = EasyJobs()
    runs.login(username="liuweibin@stonewise.cn",
               password="liuweibin@StoneWise2021",
               cloud="huawei")

    # 定义任务结构体example
    test = JobSpec("sdk-test",
                   job_type="pytorch-ddp")  # 任务命令规范：https://wiki.stonewise.cn/display/~liuweibin/submit+jobs
    test.cpu("40") \
        .mem("400Gi") \
        .gpu("8") \
        .affinity("none") \
        .image("harbor.stonewise.cn/kubeflow/transformer-3dmg-job:baseline") \
        .command("/bin/bash -c") \
        .args(
        "cd /home/jovyan/transformer-3dmg/stonewise_mg/mains/lingo3dmol/ && accelerate launch --config_file acc_config/ds_zero0.yaml --machine_rank ${RANK} --main_process_ip ${MASTER_ADDR} --main_process_port ${MASTER_PORT} --num_machines 28 --num_processes 224 --mixed_precision no --dynamo_backend no training.py --train_list /home/jovyan/wanghan_data/3DMG_data/alluxio/RComplex_96w/path.csv,/home/jovyan/wanghan_data/3DMG_data/alluxio/pdbbind2020_20230216/path.csv --eval_list /home/jovyan/wanghan_data/3DMG_data/alluxio/business/path.csv --learning_rate 1e-4 --weight_decay 0.01 --output_dir /home/jovyan/wanghan_data/transformer-3dmg/logs/rcomplex96w-1b --model_path /home/jovyan/wanghan_data/transformer-3dmg/logs/old_109w_decoder12_relf_rcomplex96w_ce_wo_leakage/0226/1/checkpoints/checkpoint_200/model.safetensors --per_gpu_train_batch_size 2 --per_gpu_eval_batch_size 2 --pocket_vocab_size 32 --ligand_vocab_size 256 --encoder_num_hidden_layers 12 --decoder_num_hidden_layers 24 --hidden_size 2048 --num_attention_heads 8 --intermediate_size 1024 --head_hidden_size 256 --head_num_hidden_layers 2 --head_relative_first --ignore_pdb_ids ''") \
        .fusevols(path="/alluxio/fuse/mol/3dmg/complex", mount_path="/home/jovyan/wanghan_data/3DMG_data/alluxio") \
        .hostvols(host_path="/kubeflow/mount/logs", mount_path="/home/jovyan/wanghan_data/transformer-3dmg/logs") \
        .retry(1) \
        .workers(27)

    # # 创建任务
    # runs.create(test)

    # # 查询任务
    # runs.get(test)  # 指定任务名称或者对象

    # 删除任务
    runs.delete(test)  # 指定任务名称或者对象

    # 查剩余资源
    runs.resources(cpu=1, memory="2Gi", gpu=1)
