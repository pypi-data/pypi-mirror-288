use pyo3::prelude::*;

#[pyclass]
#[derive(Clone)]
pub struct BertConfig {
    pub model_id: Option<String>,
    pub revision: Option<String>,
    pub chunk_size: Option<usize>,
}

#[pymethods]
impl BertConfig {
    #[new]
    #[pyo3(signature = (model_id=None, revision=None, chunk_size=None))]
    pub fn new(
        model_id: Option<String>,
        revision: Option<String>,
        chunk_size: Option<usize>,
    ) -> Self {
        Self {
            model_id,
            revision,
            chunk_size,
        }
    }
}

#[pyclass]
#[derive(Clone)]
pub struct ClipConfig {
    pub model_id: Option<String>,
    pub revision: Option<String>,
}

#[pymethods]
impl ClipConfig {
    #[new]
    #[pyo3(signature = (model_id=None, revision=None))]
    pub fn new(model_id: Option<String>, revision: Option<String>) -> Self {
        Self { model_id, revision }
    }
}

#[pyclass]
#[derive(Clone)]
pub struct OpenAIConfig {
    pub model: Option<String>,
    pub api_key: Option<String>,
    pub chunk_size: Option<usize>,
}

#[pyclass]
#[derive(Clone)]
pub struct JinaConfig {
    pub model_id: Option<String>,
    pub revision: Option<String>,
    pub chunk_size: Option<usize>,
}

#[pymethods]
impl JinaConfig {
    #[new]
    #[pyo3(signature = (model_id=None, revision=None, chunk_size=None))]
    pub fn new(
        model_id: Option<String>,
        revision: Option<String>,
        chunk_size: Option<usize>,
    ) -> Self {
        Self {
            model_id,
            revision,
            chunk_size,
        }
    }
}

#[pymethods]
impl OpenAIConfig {
    #[new]
    #[pyo3(signature = (model=None, api_key=None, chunk_size=None))]
    pub fn new(model: Option<String>, api_key: Option<String>, chunk_size: Option<usize>) -> Self {
        Self {
            model,
            api_key,
            chunk_size,
        }
    }
}

#[pyclass]
#[derive(Clone)]
pub struct AudioDecoderConfig {
    pub decoder_model_id: Option<String>,
    pub decoder_revision: Option<String>,
    pub model_type: Option<String>,
    pub quantized: Option<bool>,
}

#[pymethods]
impl AudioDecoderConfig {
    #[new]
    #[pyo3(signature = (decoder_model_id=None, decoder_revision=None, model_type=None, quantized=None))]
    pub fn new(
        decoder_model_id: Option<String>,
        decoder_revision: Option<String>,
        model_type: Option<String>,
        quantized: Option<bool>,
    ) -> Self {
        Self {
            decoder_model_id,
            decoder_revision,
            model_type,
            quantized,
        }
    }
}

#[pyclass]
#[derive(Clone, Default)]
pub struct EmbedConfig {
    pub bert: Option<BertConfig>,
    pub clip: Option<ClipConfig>,
    pub openai: Option<OpenAIConfig>,
    pub jina: Option<JinaConfig>,
    pub audio_decoder: Option<AudioDecoderConfig>,
}

#[pymethods]
impl EmbedConfig {
    #[new]
    #[pyo3(signature = (bert=None, clip=None, openai=None, jina=None, audio_decoder=None))]
    pub fn new(
        bert: Option<BertConfig>,
        clip: Option<ClipConfig>,
        openai: Option<OpenAIConfig>,
        jina: Option<JinaConfig>,
        audio_decoder: Option<AudioDecoderConfig>,
    ) -> Self {
        Self {
            bert,
            clip,
            openai,
            jina,
            audio_decoder,
        }
    }
}
