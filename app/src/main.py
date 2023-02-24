from .Layer_domain.Web import SpringerInfoCollector

# ?
def main():
    
    SIC = SpringerInfoCollector()
    SIC.collect_info('Artificial Intelligence', 200)

# ?
if __name__ == "__main__":
    main()
