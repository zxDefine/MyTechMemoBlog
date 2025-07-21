```cs
using System.Collections;
using UnityEngine;

public class GameMethods : MonoBehaviour
{
    private GameResourcesManger _gameResourcesManger;

    void Start()
    {
        _gameResourcesManger = GameObject.Find("Game Resources Manger").GetComponent<GameResourcesManger>();
    }

    // 打开贴图（携带附加设置）
    public IEnumerator OpenTexture(string textureName, bool subpixel = false, Vector2? pos = null, Vector2? anchor = null, float zoom = 0f)
    {
        // unity3d默认开启，所以可以忽略subpixel的设置
        
        Vector2 actualPos = pos ?? Vector2.zero;  // 使用默认值
        Vector2 actualAnchor = anchor ?? Vector2.zero;  // 使用默认值
       
        // 读取贴图
        TextureManager.Instance.LoadTexture(textureName);
        
        // 绘制贴图
        if (GameController.Instance.backgroundController != null)
        {
            yield return GameController.Instance.backgroundController.SetBackgroundTextureSmooth(TextureManager.Instance.Handle, actualPos, actualAnchor, zoom);
            Debug.Log("OpenTexture " + $"textureName:{textureName} subpixel:{subpixel} actualPos:{actualPos} actualAnchor:{actualAnchor} zoom:{zoom}");
        }
    }
    
    // 打开贴图(黑色)
    public IEnumerator OpenTextureBlack(float dissolve=0.0f)
    {
        if (GameController.Instance.backgroundController != null)
        {
            yield return GameController.Instance.backgroundController.OpenBackgroundColorSmooth("#000", dissolve:dissolve);
            Debug.Log("OpenTextureBlack ");
        }
    }

    // 关闭贴图
    public void CloseTexture(string textureName)
    {
        Debug.Log("CloseTexture " + textureName);
    }
    
    // 关闭贴图
    public IEnumerator CloseTextureBlack(float dissolve=0.0f)
    {
        if (GameController.Instance.backgroundController != null)
        {
            yield return GameController.Instance.backgroundController.CloseBackgroundColorSmooth(dissolve:dissolve);
            Debug.Log("CloseTextureBlack ");
        }
    }
    
    // 转场函数
    public IEnumerator TransitionDissolve(float duration)
    {
        Debug.Log("TransitionDissolve " + duration.ToString());
        
        // 模拟 dissolve 等转场特效
        yield return new WaitForSeconds(duration);
    }
    
    // 转场函数(携带参数)
    // 携带参数：ImageDissolve
    public IEnumerator Transition(string imageDissolveName)
    {
        Debug.Log("Transition " + imageDissolveName);
        
        // 模拟 dissolve 等转场特效
        // yield return new WaitForSeconds(duration);
        yield break;
    }
    
    // 设置camera
    public void SetCamera(string cameraType="None", bool perspective = true, bool gl_depth = true, Vector2? anchor= null, float xpos= 0.0f, float ypos = 0.0f, float zpos = 0.0f, float zoom = 1.0f, float blur = 0.0f, float dissolve = 0.0f)
    {
        Vector2 actualAnchor = anchor ?? Vector2.zero;  // 使用默认值
        
        Debug.Log("OpenTexture " + $"cameraType:{cameraType} perspective:{perspective} gl_depth:{gl_depth} actualAnchor:{actualAnchor} pos:({xpos}, {ypos}, {zpos}) zoom:{zoom} blur:{blur}  dissolve:{dissolve}");   
    }
    
    // 静音
    public IEnumerator SilenceSound(string soundChannel = "", float time = 0.0f)
    {
        Debug.Log($"SilenceSound {soundChannel} {time}");
        
        yield return new WaitForSeconds(time);
    }
   
    // 播放音乐
    public void PlaySound(string soundChannel = "", string soundPath = "", float silence = 0.0f, float from_start = 0.0f, float from_end = 0.0f, float volume = 0.0f, float fadeIn = 0.0f)
    {
        Debug.Log("PlaySound " + soundChannel + " " + soundPath);
        Debug.Log("Option: " + $"silence:{silence} from:({from_start}, {from_end}) volume:{volume} fadeIn:{fadeIn}");
    }
    
    // 暂停音乐
    public void StopSound(string soundChannel = "", float fadeOut = 0.0f)
    {
        Debug.Log("StopSound " + $"soundChannel:{soundChannel} fadeOut:{fadeOut}");
    }
    
    // 设置音量
    public void SetVolume(string soundChannel = "", float volume = 0.0f, float delay = 0.001f)
    {
        Debug.Log("SetVolume " + $"soundChannel:{soundChannel} volume:{volume} delay:{delay}");
    }
    
    // 更新dialog
    public IEnumerator OpenDialog(int subtitleID)
    {
        // 测试用
        string text = _gameResourcesManger.GetDialogue(subtitleID);
        bool auto = false;
        AudioClip voiceClip = null;
        
        // 打开对话框
        DialogueUI.Instance.Show(text, auto, voiceClip);
        yield return new WaitUntil(() => DialogueUI.Instance.WaitForNext());
    }
    
    ///////////////////////////////////////////////////////////////////////////////////////
    // 测试用代码
    public IEnumerator ShowDialogue(string text, bool auto = false, AudioClip voiceClip = null)
    {
        DialogueUI.Instance.Show(text, auto, voiceClip);
        yield return new WaitUntil(() => DialogueUI.Instance.WaitForNext());
            
        /////////////////////////////////// 案例
        // // 自动播放
        // yield return ShowDialogue("这是自动模式……", auto: true);
        //
        // // 播放语音 + 等待语音结束
        // AudioClip clip = Resources.Load<AudioClip>("voice/hello");
        // yield return ShowDialogue("你好，我是语音内容", voiceClip: clip);
        //
        // // 同时自动和语音都开启（语音优先）
        // yield return ShowDialogue("自动 + 语音", auto: true, voiceClip: clip);
    }

    public void Show(string imageName, ShowOptions options = null)
    {
        // 加载并展示图像，可以使用SpriteRenderer或UI Image
    }

    public void Hide(string imageName)
    {
        // 隐藏图片
    }

    public IEnumerator WaitEffect(string effectName, float duration)
    {
        // 模拟 dissolve 等转场特效
        yield return new WaitForSeconds(duration);
    }

    public IEnumerator Jump(string label)
    {
        StoryManager storyManager = GameObject.Find("Story Manager").GetComponent<StoryManager>();
        yield return storyManager.ExecuteLabel(label);
    }
}

public class ShowOptions
{
    // 你可以在这里添加显示选项的字段和方法
    public Vector2 pos;
    public Vector2 anchor;
    public float zoom;
}
```