from collections import Counter
from nvdutils.core.loaders.json_loader import JSONFeedsLoader
from nvdutils.types.options import CVEOptions, CWEOptions, CVSSOptions, DescriptionOptions, ConfigurationOptions
from nvdutils.types.configuration import CPEPart

cve_options = CVEOptions(
    cwe_options=CWEOptions(has_cwe=True, in_secondary=False, is_single=True),
    cvss_options=CVSSOptions(),
    desc_options=DescriptionOptions(),
    config_options=ConfigurationOptions(is_single_vuln_product=True, vuln_product_is_part=CPEPart.Application)
)

loader = JSONFeedsLoader(data_path='~/.nvdutils/nvd-json-data-feeds',
                         options=cve_options,
                         verbose=True)

# Populate the loader with CVE records
loader.load()

target_sw_counter = Counter()
vendor_product_pairs = set()
total_configs = 0
vulns_with_target_sw = 0

for cve_id, cve in loader.records.items():
    total_configs += len(cve.configurations)
    target_sw = cve.get_target_sw(skip_sw=['*', '-'], is_vulnerable=True)

    if len(target_sw) == 0:
        continue

    vulns_with_target_sw += 1

    # check for discrepancies in the target software
    # that means, for each key, if there are multiple values
    for key, value in target_sw.items():
        vendor_product_pairs.update(value)

        if len(value) > 1:
            print(f"{cve_id} has multiple target software for {key}: {value}")

    for sw_list in target_sw.values():
        target_sw_counter.update(sw_list)

print(target_sw_counter)
print(len(vendor_product_pairs))
print(total_configs)
print(vulns_with_target_sw)
