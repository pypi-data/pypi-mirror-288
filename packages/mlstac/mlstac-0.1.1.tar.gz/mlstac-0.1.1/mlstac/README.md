# **Machine Learning SpatioTemporal Asset Catalogs (ML-STAC)** 🤖🌐

The `ML-STAC` specification is composed of different [Pydantic Models](https://docs.pydantic.dev/latest/concepts/models/):

1. **Tensor**: Represents only ONE tensor type, chosen from `np.ndarray`, `torch.Tensor`, `jax.numpy.ndarray`, `paddle.Tensor`, and `tensorflow.Tensor`.

2. **SampleTensor**: This is linked to the `Tensor` and includes three attributes: `input`, `target`, and `extra`, all of them of the Tensor class.

3. **SampleMetadata**: Contains metadata for samples with attributes like `input`, `target`, `extra`, `geotransform`, `crs`, `id`, and date-time attributes (`start_datetime`, `end_datetime`).

4. **Sample**: Core unit to this model, an `Sample` has a `tensor` of type `SampleTensor` and `metadata` of type `SampleMetadata`.

5. **Catalog**: Comprises fields for the number of samples (`n_samples`) and a hyperlink (`url`). Each Collection must define three Catalogs: `train`, `validation`, and `test`. A Catalog can link to multiple samples, while each sample is associated with only one of the Catalogs (`train`, `validation`, or `test`).

7. **Collection**: A broader category that houses multiple catalogs (train, validation, and test). Attributes of a collection include its `name`, ML-STAC version, authorship information (`authors`), `licenses`, `split_strategy`, etc. There are additional properties like the computer vision task (`cv_task`), `sensor` details, band information (`bands`), and data type (`dtype`) for the Samples.

8. **License** and **Licenses**: Holds information about the licensing of the data, including the license name and a link. Multiple licenses can be grouped together, and additional comments can be attached.

9. **Reviewers** and **Reviewer**: These elements capture details about individuals or entities reviewing the dataset. Each reviewer has a name, a reference, a score, and an issue link. There can be multiple reviewers for a dataset.

10. **Authors** and **Author**: Detailed attributes for authors include a list of authors, details about who curated the data, and additional comments. Each author has a name, reference, and organizational affiliation.

11. **Split**: Indicates data splitting strategies such as random, stratified, cluster, systematic, or other.

12. **Task**, **Sensor**, **Bands**, and **Dtype**: These entities capture specifics about the machine learning task, the sensor used to gather the data, the bands of data, and the data type respectively.

13. **Extent**, **SpatialExtent**, and **TemporalExtent**: These components define the spatial and temporal coverage of the dataset. The spatial extent is defined by bounding boxes, while the temporal extent captures time intervals.

14. **Hyperlink**: This is a basic component that holds a URL link, utilized in various parts of the model.

The UML diagram below represents a cohesive structure, detailing how datasets in the `ML-STAC` specification are organized, catalogued, and linked together.

<p align="center">
  <img src="./assets/img/uml.png" width="100%">
</p>