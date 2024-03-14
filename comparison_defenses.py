import matplotlib.pyplot as plt
import numpy as np

# Data Preparation
rounds = np.arange(0, 11)
accuracy_median_iid = [0.1017] + [0.1] * 10
accuracy_median_non_iid = [0.1, 0.1883] + [0.1] * 9
accuracy_trimmed_iid_1mal = [0.1014, 0.2023, 0.2854, 0.3812, 0.4059, 0.4397, 0.4593, 0.4711, 0.4851, 0.5026, 0.5165]
accuracy_trimmed_iid_3mal = [0.1105] + [0.1] * 10
accuracy_trimmed_non_iid_1mal = [0.0968, 0.1926, 0.2924, 0.3513, 0.3955, 0.4158, 0.4413, 0.4579, 0.4853, 0.5003, 0.5112]
accuracy_trimmed_non_iid_3mal = [0.101, 0.2245] + [0.1] * 9
accuracy_label_flipping_iid_median = [0.1113, 0.2277, 0.3088, 0.3829, 0.4201, 0.4437, 0.4605, 0.4747, 0.4983, 0.5043, 0.5191]
accuracy_label_flipping_non_iid_median = [0.1, 0.1783, 0.261, 0.3195, 0.3694, 0.3892, 0.4134, 0.4161, 0.4473, 0.4461, 0.4727]
accuracy_label_flipping_iid_trimmed = [0.1156, 0.2328, 0.3221, 0.3716, 0.4224, 0.448, 0.4657, 0.4912, 0.4985, 0.5118, 0.5211]
accuracy_label_flipping_non_iid_trimmed = [0.0946, 0.2031, 0.2962, 0.3558, 0.397, 0.4005, 0.4215, 0.4383, 0.458, 0.4763, 0.4794]


# Plotting
plt.figure(figsize=(14, 10))

plt.subplot(2, 2, 1)
plt.plot(rounds, accuracy_median_iid, label='FedMedian IID', marker='o')
plt.plot(rounds, accuracy_trimmed_iid_1mal, label='FedTrimmedAvg IID (1 Mal)', linestyle='--', marker='x')
plt.plot(rounds, accuracy_trimmed_iid_3mal, label='FedTrimmedAvg IID (3 Mal)', linestyle='--', marker='x')
plt.title('Model Poisoning: IID Configuration')
plt.xlabel('Round')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(rounds, accuracy_median_non_iid, label='FedMedian Non-IID', marker='o')
plt.plot(rounds, accuracy_trimmed_non_iid_1mal, label='FedTrimmedAvg Non-IID (1 Mal)', linestyle='--', marker='x')
plt.plot(rounds, accuracy_trimmed_non_iid_3mal, label='FedTrimmedAvg Non-IID (3 Mal)', linestyle='--', marker='x')
plt.title('Model Poisoning: Non-IID Configuration')
plt.xlabel('Round')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(2, 2, 3)
plt.plot(rounds, accuracy_label_flipping_iid_median, label='FedMedian IID', marker='o')
plt.plot(rounds, accuracy_label_flipping_iid_trimmed, label='FedTrimmedAvg IID', linestyle='--', marker='x')
plt.title('Label Flipping: IID Configuration')
plt.xlabel('Round')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(2, 2, 4)
plt.plot(rounds, accuracy_label_flipping_non_iid_median, label='FedMedian Non-IID', marker='o')
plt.plot(rounds, accuracy_label_flipping_non_iid_trimmed, label='FedTrimmedAvg Non-IID', linestyle='--', marker='x')
plt.title('Label Flipping: Non-IID Configuration')
plt.xlabel('Round')
plt.ylabel('Accuracy')
plt.legend()


plt.savefig('defenses_impact.png')
plt.tight_layout()
plt.show()
