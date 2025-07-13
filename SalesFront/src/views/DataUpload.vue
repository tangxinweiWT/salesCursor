<template>
  <div class="data-upload">
    <el-card class="upload-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>CSV文件上传</span>
        </div>
      </template>
      
      <div class="upload-area">
        <el-upload
          ref="uploadRef"
          class="upload-demo"
          drag
          action="#"
          :auto-upload="false"
          :on-change="handleFileChange"
          :on-remove="handleFileRemove"
          :file-list="fileList"
          accept=".csv"
          :limit="1"
        >
          <el-icon class="el-icon--upload"><upload-filled /></el-icon>
          <div class="el-upload__text">
            将文件拖到此处，或<em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              只能上传 CSV 文件，且不超过 10MB
            </div>
          </template>
        </el-upload>
      </div>

      <!-- 文件预览 -->
      <div v-if="fileList.length > 0" class="file-preview">
        <h4>文件预览</h4>
        <div class="preview-table">
          <el-table :data="previewData" stripe style="width: 100%" max-height="300">
            <el-table-column 
              v-for="column in tableColumns" 
              :key="column" 
              :prop="column" 
              :label="column" 
              min-width="120"
            />
          </el-table>
        </div>
      </div>

      <!-- 上传进度 -->
      <div v-if="uploading" class="upload-progress">
        <el-progress :percentage="uploadProgress" :status="uploadStatus" />
        <p class="progress-text">{{ progressText }}</p>
      </div>

      <!-- 操作按钮 -->
      <div class="upload-actions">
        <el-button 
          type="primary" 
          :disabled="fileList.length === 0 || uploading"
          @click="handleUpload"
          :loading="uploading"
        >
          {{ uploading ? '上传中...' : '开始上传' }}
        </el-button>
        <el-button @click="resetUpload" :disabled="uploading">重置</el-button>
      </div>
    </el-card>

    <!-- 上传历史 -->
    <el-card class="upload-history" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>上传历史</span>
          <el-button type="primary" size="small" @click="loadUploadHistory">
            刷新
          </el-button>
        </div>
      </template>
      
      <el-table :data="uploadHistory" stripe style="width: 100%">
        <el-table-column prop="filename" label="文件名" />
        <el-table-column prop="uploadTime" label="上传时间" width="180" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'success' ? 'success' : 'danger'">
              {{ scope.row.status === 'success' ? '成功' : '失败' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="records" label="记录数" width="100" />
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button 
              type="text" 
              size="small" 
              @click="downloadTemplate"
            >
              下载模板
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 下载模板 -->
    <el-card class="template-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>CSV模板下载</span>
        </div>
      </template>
      
      <div class="template-info">
        <p>请按照以下格式准备CSV文件：</p>
        <el-descriptions :column="1" border>
          <el-descriptions-item label="日期">YYYY-MM-DD 格式，如：2024-01-01</el-descriptions-item>
          <el-descriptions-item label="产品名称">产品的中文名称</el-descriptions-item>
          <el-descriptions-item label="分类">产品分类，如：电子产品、服装等</el-descriptions-item>
          <el-descriptions-item label="数量">销售数量，整数</el-descriptions-item>
          <el-descriptions-item label="单价">产品单价，保留两位小数</el-descriptions-item>
          <el-descriptions-item label="总金额">总金额，保留两位小数</el-descriptions-item>
        </el-descriptions>
        
        <div class="template-download">
          <el-button type="success" @click="downloadTemplate">
            <el-icon><Download /></el-icon>
            下载CSV模板
          </el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { salesAPI } from '@/api'

export default {
  name: 'DataUpload',
  setup() {
    const uploadRef = ref()
    const fileList = ref([])
    const previewData = ref([])
    const tableColumns = ref([])
    const uploading = ref(false)
    const uploadProgress = ref(0)
    const uploadStatus = ref('')
    const progressText = ref('')
    const uploadHistory = ref([])

    // 处理文件选择
    const handleFileChange = (file) => {
      if (file.raw.size > 10 * 1024 * 1024) {
        ElMessage.error('文件大小不能超过10MB')
        return false
      }
      
      // 读取CSV文件内容进行预览
      const reader = new FileReader()
      reader.onload = (e) => {
        const csv = e.target.result
        const lines = csv.split('\n')
        const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''))
        tableColumns.value = headers
        
        // 预览前5行数据
        const preview = []
        for (let i = 1; i < Math.min(6, lines.length); i++) {
          if (lines[i].trim()) {
            const values = lines[i].split(',').map(v => v.trim().replace(/"/g, ''))
            const row = {}
            headers.forEach((header, index) => {
              row[header] = values[index] || ''
            })
            preview.push(row)
          }
        }
        previewData.value = preview
      }
      reader.readAsText(file.raw)
    }

    // 处理文件移除
    const handleFileRemove = () => {
      previewData.value = []
      tableColumns.value = []
    }

    // 处理上传
    const handleUpload = async () => {
      if (fileList.value.length === 0) {
        ElMessage.warning('请先选择文件')
        return
      }

      try {
        uploading.value = true
        uploadProgress.value = 0
        uploadStatus.value = ''
        progressText.value = '准备上传...'

        const file = fileList.value[0].raw
        
        // 模拟上传进度
        const progressInterval = setInterval(() => {
          if (uploadProgress.value < 90) {
            uploadProgress.value += 10
            progressText.value = `上传中... ${uploadProgress.value}%`
          }
        }, 200)

        const result = await salesAPI.uploadCSV(file)
        
        clearInterval(progressInterval)
        uploadProgress.value = 100
        uploadStatus.value = 'success'
        progressText.value = '上传完成！'

        ElMessage.success('文件上传成功！')
        
        // 重置上传状态
        setTimeout(() => {
          resetUpload()
          loadUploadHistory()
        }, 2000)

      } catch (error) {
        uploadStatus.value = 'exception'
        progressText.value = '上传失败'
        ElMessage.error('文件上传失败：' + (error.message || '未知错误'))
      } finally {
        uploading.value = false
      }
    }

    // 重置上传
    const resetUpload = () => {
      fileList.value = []
      previewData.value = []
      tableColumns.value = []
      uploadProgress.value = 0
      uploadStatus.value = ''
      progressText.value = ''
      if (uploadRef.value) {
        uploadRef.value.clearFiles()
      }
    }

    // 加载上传历史
    const loadUploadHistory = async () => {
      try {
        // 这里应该调用API获取上传历史
        // const history = await salesAPI.getUploadHistory()
        // uploadHistory.value = history
        
        // 模拟数据
        uploadHistory.value = [
          {
            filename: 'sales_data_2024.csv',
            uploadTime: '2024-01-15 10:30:00',
            status: 'success',
            records: 1250
          },
          {
            filename: 'sales_data_2023.csv',
            uploadTime: '2024-01-10 14:20:00',
            status: 'success',
            records: 980
          }
        ]
      } catch (error) {
        console.error('加载上传历史失败:', error)
      }
    }

    // 下载模板
    const downloadTemplate = () => {
      const csvContent = '日期,产品名称,分类,数量,单价,总金额\n2024-01-01,示例产品,电子产品,1,99.99,99.99'
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
      const link = document.createElement('a')
      const url = URL.createObjectURL(blob)
      link.setAttribute('href', url)
      link.setAttribute('download', 'sales_template.csv')
      link.style.visibility = 'hidden'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }

    onMounted(() => {
      loadUploadHistory()
    })

    return {
      uploadRef,
      fileList,
      previewData,
      tableColumns,
      uploading,
      uploadProgress,
      uploadStatus,
      progressText,
      uploadHistory,
      handleFileChange,
      handleFileRemove,
      handleUpload,
      resetUpload,
      loadUploadHistory,
      downloadTemplate
    }
  }
}
</script>

<style scoped>
.data-upload {
  padding: 0;
}

.upload-card,
.upload-history,
.template-card {
  margin-bottom: 24px;
  transition: all 0.2s ease;
  border: 1px solid #f0f0f0;
}

.upload-card:hover,
.upload-history:hover,
.template-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1) !important;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: #fafafa;
  border-bottom: 1px solid #f0f0f0;
  margin: -20px -20px 20px -20px;
}

.card-header span {
  font-weight: 600;
  color: #333333;
  font-size: 16px;
}

.upload-area {
  margin-bottom: 24px;
}

.upload-demo {
  width: 100%;
}

.upload-demo .el-upload-dragger {
  border-radius: 8px;
  border: 2px dashed #d9d9d9;
  background: #fafafa;
  transition: all 0.2s ease;
}

.upload-demo .el-upload-dragger:hover {
  border-color: #1890ff;
  background: #f0f8ff;
}

.file-preview {
  margin: 24px 0;
  padding: 20px;
  background: #fafafa;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
}

.file-preview h4 {
  margin-bottom: 16px;
  color: #333333;
  font-weight: 600;
  font-size: 16px;
}

.preview-table {
  max-height: 300px;
  overflow-y: auto;
  border-radius: 8px;
}

.upload-progress {
  margin: 24px 0;
  padding: 20px;
  background: #f6ffed;
  border-radius: 8px;
  border: 1px solid #b7eb8f;
}

.progress-text {
  margin-top: 12px;
  text-align: center;
  color: #333333;
  font-weight: 500;
}

.upload-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-top: 24px;
  padding: 20px;
  background: #fafafa;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
}

.template-info {
  line-height: 1.6;
}

.template-info p {
  margin-bottom: 16px;
  color: #666666;
  font-weight: 500;
}

.template-download {
  margin-top: 24px;
  text-align: center;
  padding: 20px;
  background: #f6ffed;
  border-radius: 8px;
  border: 1px solid #b7eb8f;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .upload-actions {
    flex-direction: column;
  }
  
  .upload-actions .el-button {
    width: 100%;
  }
}
</style> 