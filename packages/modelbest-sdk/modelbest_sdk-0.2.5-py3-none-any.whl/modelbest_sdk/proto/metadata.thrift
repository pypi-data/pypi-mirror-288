namespace py proto
namespace cpp proto

enum TableType {
    RECORD_TABLE = 0,
    LIST_TABLE =1,
}

// tag 1 is reserved.
struct SSTableMetadata {
    2: optional i32 total_count,           // total number of sstable records.
    3: optional string tokenizer_version,  // tokenizer_version used to generate tokens in sstable.
    4: optional string proto_type,         // The proto type of sstable record.
    5: optional TableType tabletype,       // enum type table_type.
}
